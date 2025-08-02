from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, DoubleType, StringType

# 1) Crée la session Spark
spark = SparkSession.builder \
    .appName("RealTimeAnomalyDetection") \
    .getOrCreate()

# 2) Schéma des transactions (adapter à ton JSON)
schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("amount", DoubleType()),
    StructField("timestamp", StringType()),
    # ajoute d'autres champs si besoin…
])

# 3) Lit en continu depuis Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "transactions") \
    .load()

# 4) Décode la colonne value (JSON) et la transforme
json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# 5) Charge ton scaler et tes modèles
from joblib import load
scaler = load("/opt/bitnami/spark/app/models/scaler.pkl")
# si tu utilises un auto-encoder Keras :
# from tensorflow.keras.models import load_model
# ae = load_model("/opt/bitnami/spark/app/models/autoencoder_model.keras")

# Fonction UDF pour mettre à l’échelle et prédire :
from pyspark.sql.functions import pandas_udf, PandasUDFType
import pandas as pd

@pandas_udf("double", PandasUDFType.SCALAR)
def detect_anomaly(amounts: pd.Series) -> pd.Series:
    X = scaler.transform(amounts.to_frame())
    # preds = ae.predict(X)  # ou isolation_forest.predict(X)
    # return pd.Series((preds > threshold).astype(float))
    # ici on renvoie juste l’amount pour l’exemple
    return amounts

# 6) Applique la détection
result = json_df.withColumn("anomaly_score", detect_anomaly(col("amount")))

# 7) Écrit le résultat sur la console (ou un sink de ton choix)
query = result.writeStream \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
