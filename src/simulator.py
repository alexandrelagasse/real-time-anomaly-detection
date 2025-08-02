# src/simulator.py

import json
import time
import pandas as pd
from kafka import KafkaProducer

# 1. Charger les données
df = pd.read_csv("data/cleaned_creditcard.csv")
# Si tu veux un flux plus long/répété, tu pourras faire plusieurs epochs ou shuffle.

# 2. Initialiser le producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

topic = "transactions"

# 3. Envoyer chaque transaction
for idx, row in df.iterrows():
    message = row.drop("Class").to_dict()  # on n’envoie pas le label
    producer.send(topic, value=message)
    print(f"Sent record {idx}", end="\r")
    time.sleep(0.1)  # 10 messages par seconde

producer.flush()
print("\n✅ Simulation terminée")
