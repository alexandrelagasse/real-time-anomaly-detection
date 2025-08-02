# Détection d'Anomalies en Temps Réel - Transactions Bancaires

Un système complet de détection d'anomalies en temps réel pour les transactions bancaires, utilisant une architecture MLOps moderne et déployable gratuitement.

## Objectifs du Projet

- **Détection d'anomalies** sur transactions bancaires en temps réel
- **Architecture MLOps complète** avec tracking, monitoring et déploiement
- **Stack 100% gratuite** déployable en local et cloud
- **UX professionnelle** avec dashboard et monitoring en live

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Génération    │    │   Streaming     │    │   Traitement    │
│   de Flux       │───▶│   Kafka         │───▶│   PySpark       │
│   (Python)      │    │   (Docker)      │    │   Structured    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Monitoring    │    │   ML Tracking   │    │   Modèle ML     │
│   Grafana       │◀───│   MLflow        │◀───│   Isolation     │
│   + InfluxDB    │    │   (Docker)      │    │   Forest        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Stack Technique

| Composant | Technologie | Justification |
|-----------|------------|---------------|
| **Génération de flux** | Python + Faker + Confluent-Kafka | Léger et gratuit |
| **Streaming/Ingestion** | Apache Kafka (Docker) | Standard industrie |
| **Traitement temps réel** | PySpark Structured Streaming | Pro, scalable |
| **Modèle de détection** | Isolation Forest (scikit-learn) | Robuste, simple |
| **ML Tracking/MLOps** | MLflow (Docker) | Gratuit, complet |
| **Monitoring dashboard** | Grafana + InfluxDB (Docker) | Visualisation en live |
| **Orchestration** | Docker Compose | Tout en local, reproductible |
| **Cloud (optionnel)** | Render/Railway | Hébergement gratuit |
| **CI/CD (optionnel)** | GitHub Actions | Tests automatiques |

## Structure du Projet

```
real-time-anomaly-detection/
├── src/
│   ├── data_generator/     # Génération de flux de données
│   ├── streaming/          # Traitement Kafka + PySpark
│   ├── ml/                # Modèles et entraînement
│   └── monitoring/        # Dashboard et alertes
├── notebooks/             # Exploration et développement
├── docker/               # Configurations Docker
├── mlruns/              # Expériences MLflow
├── data/                # Datasets et données
├── requirements.txt      # Dépendances Python
├── docker-compose.yml   # Orchestration complète
└── README.md           # Documentation
```

## Installation et Démarrage

### Prérequis
- Docker et Docker Compose
- Python 3.8+
- Git

### Installation Rapide

```bash
# Cloner le projet
git clone <repository-url>
cd real-time-anomaly-detection

# Démarrer l'infrastructure complète
docker-compose up -d

# Installer les dépendances Python
pip install -r requirements.txt

# Lancer le système
python src/main.py
```

### Accès aux Services

- **Grafana Dashboard**: http://localhost:3000
- **MLflow Tracking**: http://localhost:5000
- **Kafka UI**: http://localhost:8080

## Configuration

### Variables d'Environnement

```bash
# .env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
MLFLOW_TRACKING_URI=http://localhost:5000
GRAFANA_URL=http://localhost:3000
```

### Configuration Docker

```yaml
# docker-compose.yml
version: '3.8'
services:
  kafka:
    image: confluentinc/cp-kafka:latest
    # ... configuration Kafka
  
  mlflow:
    image: python:3.8
    # ... configuration MLflow
  
  grafana:
    image: grafana/grafana:latest
    # ... configuration Grafana
```

## Fonctionnalités

### Détection d'Anomalies
- **Isolation Forest** pour détection non-supervisée
- **Seuils adaptatifs** basés sur l'historique
- **Alertes en temps réel** via Kafka

### Monitoring
- **Dashboard Grafana** avec métriques en live
- **Tracking MLflow** pour les expériences
- **Alertes automatiques** sur anomalies

### Pipeline MLOps
- **Entraînement automatique** des modèles
- **Versioning** des modèles avec MLflow
- **Déploiement continu** via Docker

## Utilisation

### Génération de Données

```python
from src.data_generator import TransactionGenerator

# Générer des transactions en temps réel
generator = TransactionGenerator()
generator.start_streaming()
```

### Détection d'Anomalies

```python
from src.ml.anomaly_detector import AnomalyDetector

# Détecter les anomalies
detector = AnomalyDetector()
anomalies = detector.detect_anomalies(transaction_data)
```

### Monitoring

```python
from src.monitoring import MetricsCollector

# Collecter les métriques
collector = MetricsCollector()
collector.log_metrics(predictions, actual)
```

## Métriques et KPIs

- **Précision de détection**: > 95%
- **Latence de traitement**: < 100ms
- **Throughput**: > 1000 transactions/sec
- **Faux positifs**: < 2%

## Déploiement

### Local
```bash
docker-compose up -d
```

### Cloud (Render/Railway)
```bash
# Configuration automatique via docker-compose
# Déploiement en un clic
```

## Tests

```bash
# Tests unitaires
python -m pytest tests/

# Tests d'intégration
python -m pytest tests/integration/

# Tests de performance
python -m pytest tests/performance/
```

## Documentation

- [Guide d'installation détaillé](docs/installation.md)
- [Architecture technique](docs/architecture.md)
- [API Reference](docs/api.md)
- [Troubleshooting](docs/troubleshooting.md)

## Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

**Votre Nom** - [LinkedIn](https://linkedin.com/in/votre-profil) - [GitHub](https://github.com/votre-username)

## Remerciements

- [MLflow](https://mlflow.org/) pour le tracking ML
- [Apache Kafka](https://kafka.apache.org/) pour le streaming
- [Grafana](https://grafana.com/) pour le monitoring
- [Docker](https://www.docker.com/) pour la containerisation

---

**Star ce projet si il vous a été utile !**
