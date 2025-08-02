#!/usr/bin/env bash

echo "🚀 Démarrage complet du système de détection d'anomalies"
echo "========================================================"
echo ""
echo "🏗️  Infrastructure complète dans Docker:"
echo "   - Zookeeper + Kafka"
echo "   - Spark Master + Worker"  
echo "   - Générateur de transactions"
echo "   - Détecteur d'anomalies Z-Score"
echo ""
echo "📺 Tous les logs seront affichés dans cette fenêtre"
echo "⏹️  Pour arrêter: Ctrl+C"
echo ""

# Nettoyer d'abord
echo "🧹 Nettoyage..."
docker-compose down --volumes --remove-orphans

echo ""
echo "🔨 Construction et lancement..."

# Démarrer tout le système
docker-compose up --build