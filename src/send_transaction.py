#!/usr/bin/env python3
"""
Générateur de transactions pour tester la détection d'anomalies
Envoie depuis Windows vers Kafka dans Docker
"""

import json
import time
import uuid
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

print("🚀 Générateur de transactions pour détection d'anomalies")
print("=======================================================")
print("📊 Transactions normales: 20-200€")
print("🚨 Anomalies artificielles: >500€ ou <5€ (15% de chance)")
print("")

kafka_host = 'kafka:9092' if os.getenv('DOCKER_ENV') or 'app' in os.getcwd() else 'localhost:9092'

print(f"🔗 Connexion Kafka: {kafka_host}")

producer = KafkaProducer(
    bootstrap_servers=[kafka_host],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retry_backoff_ms=1000,
    retries=5,
    request_timeout_ms=30000,
    acks='all'
)

def generate_transaction(tx_counter):
    """Retourne une transaction normale ou anormale."""
    

    is_anomaly = random.random() < 0.15
    
    if is_anomaly:
        amount = random.choice([
            random.uniform(500, 1000),  # Très élevé
            random.uniform(0.01, 4.99), # Très faible
        ])
        status = "🚨 ANOMALIE"
    else:
        amount = random.uniform(20, 200)
        status = "✅ Normal"
    
    return {
        "transaction_id": f"win_{tx_counter:06d}",
        "amount": round(amount, 2),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }, status

if __name__ == "__main__":
    print("🔄 Envoi continu de transactions vers Kafka… Ctrl+C pour arrêter")
    print("")
    
    tx_counter = 1
    total_anomalies = 0
    
    try:
        while True:
            tx, status = generate_transaction(tx_counter)
            
            future = producer.send("transactions", tx)
            
            if "ANOMALIE" in status:
                total_anomalies += 1
            
            anomaly_rate = (total_anomalies / tx_counter) * 100
            print(f"{status} | {tx['transaction_id']} | {tx['amount']}€ | Rate: {anomaly_rate:.1f}%")
            
            producer.flush()
            
            tx_counter += 1
            time.sleep(2)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Arrêt du producer")
        print(f"📊 Statistiques finales:")
        print(f"   - Total transactions: {tx_counter - 1}")
        print(f"   - Anomalies générées: {total_anomalies}")
        print(f"   - Taux d'anomalies: {(total_anomalies / max(1, tx_counter - 1)) * 100:.1f}%")
        producer.close()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        producer.close()
