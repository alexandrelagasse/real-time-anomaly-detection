#!/usr/bin/env python3
"""
Générateur de données de test simple pour tester la détection d'anomalies
Usage: python3 generate_test_data.py
"""

import json
import time
import random
from datetime import datetime

def send_to_kafka_via_docker(message):
    """Envoie un message à Kafka via docker-compose exec"""
    import subprocess
    
    cmd = [
        "docker-compose", "exec", "-T", "kafka", 
        "kafka-console-producer",
        "--broker-list", "kafka:9092",
        "--topic", "transactions"
    ]
    
    try:
        proc = subprocess.run(
            cmd, 
            input=json.dumps(message).encode(), 
            capture_output=True,
            timeout=10
        )
        return proc.returncode == 0
    except Exception as e:
        print(f"❌ Erreur envoi Kafka: {e}")
        return False

def generate_transaction(tx_id, anomaly_rate=0.1):
    """Génère une transaction normale ou anormale"""
    
    is_anomaly = random.random() < anomaly_rate
    
    if is_anomaly:
        # Montants anormaux 
        amount = random.choice([
            random.uniform(500, 1000),  # Très élevé
            random.uniform(0.01, 5),    # Très faible
        ])
        status = "🚨 ANOMALIE"
    else:
        # Montants normaux 
        amount = random.uniform(20, 200)
        status = "✅ Normal"
    
    transaction = {
        "transaction_id": f"tx_{tx_id:06d}",
        "amount": round(amount, 2),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return transaction, status

def main():
    print("🎲 Générateur de données de test")
    print("================================")
    print("📊 Transactions normales: 20-200€")
    print("🚨 Anomalies: >500€ ou <5€ (10% de chance)")
    print("⚡ Une transaction toutes les 3 secondes")
    print("⏹️  Pour arrêter: Ctrl+C")
    print("")
    
    tx_id = 1
    
    try:
        while True:
            transaction, status = generate_transaction(tx_id)
            
            success = send_to_kafka_via_docker(transaction)
            
            if success:
                print(f"{status} | {transaction['transaction_id']} | {transaction['amount']}€ | ✅ Envoyé")
            else:
                print(f"❌ Échec envoi | {transaction['transaction_id']} | {transaction['amount']}€")
            
            tx_id += 1
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n⏹️  Arrêt du générateur")
        print(f"📊 {tx_id - 1} transactions générées")

if __name__ == "__main__":
    main()