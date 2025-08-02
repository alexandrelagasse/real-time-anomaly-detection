#!/bin/bash

echo "🚀 Démarrage du pipeline Spark de détection d'anomalies (Z-Score pur)"

# Plus besoin de modèles ! Tout en Spark SQL natif 🎉
echo "✨ Avantages de cette approche :"
echo "   - Pas de numpy/sklearn"
echo "   - Pas de dépendances C/compilation"
echo "   - 100% Spark natif"
echo "   - Ultra-rapide et scalable"

# Lancer le job Spark avec Z-Score
echo "⚡ Lancement du job Spark (Z-Score detection)..."
spark-submit \
    --master spark://spark-master:7077 \
    --conf spark.sql.streaming.statefulOperator.checkCorrectness.enabled=false \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
    /opt/bitnami/spark/app/src/spark_stream.py

echo "✅ Pipeline terminé"