# Détection d'Anomalies en Temps Réel - Transactions Bancaires

Un prototype de système de détection d'anomalies pour transactions bancaires utilisant Apache Spark et différents algorithmes de machine learning.

## Objectifs du Projet

- **Expérimentation** avec différents modèles de détection d'anomalies
- **Streaming en temps réel** avec Apache Spark Structured Streaming
- **Comparaison de modèles** pour identifier les meilleures performances
- **Pipeline de données** pour le traitement de transactions

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Génération    │    │   Streaming     │    │   Comparaison   │
│   Transactions  │───▶│   Apache Spark  │───▶│   de Modèles    │
│   (Python)      │    │   Structured    │    │   (ML)          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Stack Technique

| Composant | Technologie | Usage |
|-----------|------------|-------|
| **Traitement streaming** | Apache Spark (PySpark) | Traitement temps réel |
| **Génération de données** | Python + Faker | Simulation de transactions |
| **Modèles ML** | scikit-learn | Détection d'anomalies |
| **Orchestration** | Docker + Scripts shell | Démarrage services |
| **Exploration** | Jupyter Notebooks | Analyse exploratoire |

## Structure du Projet

```
real-time-anomaly-detection/
├── src/
│   ├── compare_models.py    # Comparaison d'algorithmes ML
│   ├── send_transaction.py  # Générateur de transactions
│   └── spark_stream.py      # Pipeline Spark Streaming
├── data/
│   └── grep_data.py        # Utilitaires données
├── notebooks/
│   └── 01_eda_and_preprocessing.ipynb  # Analyse exploratoire
├── models/                 # Modèles sauvegardés (vide)
├── logs_sender.sh         # Script logs envoi
├── logs_spark.sh          # Script logs Spark
├── start_all.sh           # Démarrage complet
├── start_spark.sh         # Démarrage Spark
├── run_all.sh             # Exécution pipeline
├── docker-compose.yml     # Services Docker
├── Dockerfile             # Configuration container
├── requirements.txt       # Dépendances Python
└── README.md             # Documentation
```

## Installation et Démarrage

### Prérequis
- Docker et Docker Compose
- Python 3.8+
- Apache Spark (inclus dans Docker)

### Installation Rapide

```bash
# Cloner le projet
git clone <repository-url>
cd real-time-anomaly-detection

# Installer les dépendances Python
pip install -r requirements.txt

# Démarrer tous les services
./start_all.sh

# Ou lancer le pipeline complet
./run_all.sh
```

### Scripts Disponibles

- `./start_all.sh` - Démarre tous les services Docker
- `./start_spark.sh` - Démarre uniquement Spark
- `./run_all.sh` - Exécute le pipeline complet
- `./logs_spark.sh` - Affiche les logs Spark
- `./logs_sender.sh` - Affiche les logs d'envoi

## Configuration

Le projet utilise Docker Compose pour orchestrer les services. La configuration principale se trouve dans `docker-compose.yml`.

### Services Docker
- **Spark Master/Worker** - Traitement distribué
- **Jupyter** - Notebooks d'exploration
- **Application Python** - Pipeline de données

## Fonctionnalités

### Génération de Données
- **Simulation de transactions** bancaires réalistes
- **Flux continu** de données avec `send_transaction.py`
- **Patterns normaux et anomalies** intégrés

### Traitement Streaming
- **Apache Spark Structured Streaming** 
- **Pipeline temps réel** avec `spark_stream.py`
- **Traitement par micro-batches**

### Détection d'Anomalies
- **Comparaison de modèles** ML avec `compare_models.py`
- **Algorithmes multiples** (Isolation Forest, One-Class SVM, etc.)
- **Évaluation de performances** automatisée

## Utilisation

### Génération de Transactions

```bash
# Lancer la génération de données
python src/send_transaction.py
```

### Pipeline Spark Streaming

```bash
# Démarrer le traitement en temps réel
python src/spark_stream.py
```

### Comparaison de Modèles

```bash
# Comparer les algorithmes de détection
python src/compare_models.py
```

### Exploration des Données

```bash
# Ouvrir Jupyter pour l'analyse
docker-compose exec jupyter jupyter notebook
# Puis ouvrir: notebooks/01_eda_and_preprocessing.ipynb
```

## Composants Principaux

- **`send_transaction.py`** - Génère un flux de transactions simulées
- **`spark_stream.py`** - Traite les données en streaming avec Spark
- **`compare_models.py`** - Compare différents algorithmes ML
- **Notebook EDA** - Analyse exploratoire et préprocessing

## Déploiement

### Local
```bash
# Démarrer l'environnement complet
./start_all.sh

# Ou étape par étape
docker-compose up -d
./run_all.sh
```

## Développement

Ce projet est un **prototype d'expérimentation** pour la détection d'anomalies. Il permet de :

- Tester différents algorithmes de ML
- Expérimenter avec Spark Streaming  
- Analyser des données de transactions simulées
- Comparer les performances des modèles

### Prochaines étapes possibles

- Intégration avec une vraie source de données
- Ajout de plus d'algorithmes de détection
- Interface web pour visualiser les résultats
- Système d'alertes en temps réel
- Optimisation des performances

## Structure des Données

Les transactions générées incluent :
- ID utilisateur et marchand
- Montant et devise
- Coordonnées géographiques
- Timestamp
- Labels d'anomalies

## Technologies Utilisées

- **Apache Spark** - Traitement distribué
- **Python** - Logique métier et ML
- **Docker** - Containerisation
- **Jupyter** - Exploration de données
- **scikit-learn** - Algorithmes ML

---

**Projet d'expérimentation en détection d'anomalies - 2025**
