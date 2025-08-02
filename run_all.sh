#!/usr/bin/env bash
set -e

echo "🚀 Script de lancement complet du système de détection d'anomalies"
echo "=================================================================="

# 1) Démarre les conteneurs en arrière-plan
echo "🚀 Lancement des services Docker..."
docker-compose up -d

# 2) Attends que Kafka soit prêt
echo -n "⏳ Attente de Kafka..."
until docker-compose exec kafka \
  kafka-topics --bootstrap-server kafka:9092 --list > /dev/null 2>&1; do
  echo -n "."
  sleep 1
done
echo " ✅"

# 3) (Re)création du topic transactions
echo "📑 Création du topic Kafka 'transactions' (si besoin)..."
docker-compose exec kafka kafka-topics \
  --bootstrap-server kafka:9092 \
  --create \
  --topic transactions \
  --partitions 1 \
  --replication-factor 1 \
  2> /dev/null || true

# 4) Envoi d'un message de test
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "✉️ Envoi d'un message test sur 'transactions'..."
echo "{\"transaction_id\":\"tx-test\",\"amount\":123.45,\"timestamp\":\"${TS}\"}" \
  | docker-compose exec -T kafka kafka-console-producer \
      --broker-list kafka:9092 \
      --topic transactions

# 5) Lecture du premier message pour vérifier
echo "🔍 Lecture du message depuis le début..."
docker-compose exec kafka kafka-console-consumer \
  --bootstrap-server kafka:9092 \
  --topic transactions \
  --from-beginning \
  --max-messages 1

echo ""
echo "✅ Topic 'transactions' créé et testé avec succès !"
echo ""

# 6) Lancement du job Spark (en arrière-plan ou interactif)
echo "🔥 Lancement du job Spark de détection d'anomalies..."
echo "   💡 Mode Z-Score pur Spark SQL (sans numpy/sklearn)"
echo "   🛡️  Protection division par zéro activée"
echo "   🕒 Timezone UTC configurée"
echo ""
echo "📺 Pour voir les anomalies détectées, les logs s'afficheront ci-dessous"
echo "⏹️  Pour arrêter: CTRL+C"
echo ""

# Utilisation de notre script start_spark.sh optimisé
docker-compose exec spark-master bash /opt/bitnami/spark/app/start_spark.sh

# Remarque : ce dernier 'spark-submit' bloque en mode streaming.
# Pour stopper proprement, faites CTRL+C dans ce terminal.