#!/usr/bin/env bash

echo "📺 Logs Générateur de Transactions"
echo "=================================="
echo "🎲 Suivi des transactions envoyées"
echo "⏹️  Pour arrêter: Ctrl+C"
echo ""

# Suivre les logs du générateur de données
docker-compose logs -f sender