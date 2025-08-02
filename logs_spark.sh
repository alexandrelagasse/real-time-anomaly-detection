#!/usr/bin/env bash

echo "📺 Logs Spark - Détection d'anomalies en temps réel"
echo "=================================================="
echo "🔍 Recherche: anomaly, z_score, transactions"
echo "⏹️  Pour arrêter: Ctrl+C"
echo ""

# Suivre les logs Spark avec filtrage intelligent
docker-compose logs -f spark-master | grep -E "(anomaly|z_score|transaction_id|🚨|✅|📊|ERROR|Exception)" --color=always