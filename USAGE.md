# 🚀 Système de Détection d'Anomalies en Temps Réel

## Architecture Ultra-Simplifiée ✨

- **100% Spark SQL natif** - Pas de numpy/sklearn/joblib
- **Z-Score pur** - Détection d'anomalies par écart statistique  
- **Kafka + Spark Streaming** - Pipeline temps réel scalable
- **Docker tout-en-un** - Infrastructure complète en local

## Démarrage Rapide ⚡

### 1. Lancer tout le système

```bash
# Rendre le script exécutable (première fois)
chmod +x run_all.sh

# Lancer l'infrastructure complète
./run_all.sh
```

Ce script va :
- ✅ Démarrer Kafka + Spark
- ✅ Créer le topic `transactions`  
- ✅ Tester la connectivité
- ✅ Lancer la détection d'anomalies

### 2. Générer des données de test

Dans un **autre terminal** :

```bash
python3 generate_test_data.py
```

Cela va envoyer :
- 📊 Transactions normales : 20-200€
- 🚨 Anomalies artificielles : >500€ ou <5€ (10% de chance)

## Comment ça fonctionne 🔬

### Détection Z-Score

```sql
z_score = |amount - moyenne_fenêtre| / ecart_type_fenêtre
anomalie = z_score > 3.0
```

### Fenêtres temporelles

- **Fenêtre** : 1 minute  
- **Slide** : 30 secondes
- **Watermark** : 5 minutes (tolérance late data)

### Sortie

Le système affiche en temps réel :
- Toutes les transactions avec leur z-score
- Filtrage spécial des anomalies détectées

## Surveillance 📊

### Logs Spark
```bash
docker-compose logs -f spark-master
```

### Interfaces Web
- **Spark Master** : http://localhost:8080  
- **Spark Worker** : http://localhost:8081

### Topics Kafka
```bash
# Lister les topics
docker-compose exec kafka kafka-topics --bootstrap-server kafka:9092 --list

# Consommer les messages
docker-compose exec kafka kafka-console-consumer \
  --bootstrap-server kafka:9092 \
  --topic transactions \
  --from-beginning
```

## Arrêt du système ⏹️

```bash
# Arrêter proprement
docker-compose down

# Nettoyage complet (volumes inclus)
docker-compose down --volumes
```

## Avantages de cette approche ✅

1. **Zéro dépendance Python complexe** - Plus de problèmes numpy/_core
2. **Ultra-rapide** - Calculs natifs Spark, pas de sérialisation Python  
3. **Scalable** - Peut traiter des millions de transactions
4. **Production-ready** - Watermarks, checkpoints, gestion d'erreurs
5. **Simple** - Une seule commande pour tout démarrer

## Personnalisation 🎛️

### Changer le seuil d'anomalie
Dans `src/spark_stream.py` :
```python
ANOMALY_THRESHOLD = 3.0  # Modifier cette valeur
```

### Ajuster les fenêtres
```python
window(col("timestamp"), "1 minute", "30 seconds")  # durée, slide
```

### Modifier le watermark  
```python
.withWatermark("timestamp", "5 minutes")  # tolérance late data
```

🎉 **Système prêt pour la production !**