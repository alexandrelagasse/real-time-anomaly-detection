from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, stddev, abs, when, window, to_timestamp, greatest, lit
from pyspark.sql.types import StructType, StructField, DoubleType, StringType, TimestampType

# 1) Crée la session Spark avec toutes les optimisations
spark = SparkSession.builder \
    .appName("RealTimeAnomalyDetection") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .config("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", "false") \
    .config("spark.sql.session.timeZone", "UTC") \
    .getOrCreate()

# Réduire le niveau de logs pour éviter le spam
spark.sparkContext.setLogLevel("WARN")

print("✅ Session Spark configurée:")
print("   - Contrôle de correctness désactivé")
print("   - Timezone fixée à UTC")
print("   - Logs réduits au niveau WARN")

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
    .option("startingOffsets", "latest") \
    .load()

# 4) Décode la colonne value (JSON) et la transforme
json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("timestamp", to_timestamp(col("timestamp")))

print("🚀 Démarrage de la détection d'anomalies avec Z-Score pur Spark SQL...")

# 5) Détection d'anomalies avec Z-Score + Watermark (sans numpy/sklearn !)
# Seuil: si |amount - moyenne| > 3 * écart-type → anomalie
ANOMALY_THRESHOLD = 3.0

print("🔧 Configuration de la détection par fenêtres temporelles...")

# 1) Ajout d'un watermark sur le timestamp (5 minutes de tolérance pour late data)
stream_with_watermark = json_df.withWatermark("timestamp", "5 minutes")

# 2) Créer la colonne window sur les événements
events_with_window = stream_with_watermark.select(
    "transaction_id",
    "amount", 
    "timestamp",
    window(col("timestamp"), "1 minute", "30 seconds").alias("window")
)

print("📊 Calcul des statistiques par fenêtre de 1 minute...")

# 3) Statistiques par fenêtre avec protection contre division par zéro
SAFE_STD = 1e-9  # Écart-type minimum pour éviter division par zéro

windowed_stats = events_with_window \
    .groupBy("window") \
    .agg(
        avg("amount").alias("mean_amount"),
        stddev("amount").alias("std_amount")
    ) \
    .withColumn(
        "std_amount_safe", 
        greatest(col("std_amount"), lit(SAFE_STD))
    )

print("🛡️  Protection contre division par zéro activée (std min = 1e-9)")

# 4) Joindre les événements avec les stats via la colonne window
result = events_with_window \
    .join(windowed_stats, on="window") \
    .withColumn(
        "z_score", 
        abs(col("amount") - col("mean_amount")) / col("std_amount_safe")
    ) \
    .withColumn(
        "is_anomaly",
        when(col("z_score") > ANOMALY_THRESHOLD, 1.0).otherwise(0.0)
    ) \
    .select(
        "transaction_id",
        "amount", 
        "timestamp",
        "window",
        "mean_amount",
        "std_amount_safe", 
        "z_score", 
        "is_anomaly"
    )

# 6) Filtrer uniquement les anomalies pour l'affichage
anomalies_only = result.filter(col("is_anomaly") == 1.0)

# 7) Écrit le résultat sur la console en mode append (maintenant compatible !)
print("📊 Affichage de toutes les transactions avec scores d'anomalie...")
print("   ✅ Mode append compatible grâce au watermark + fenêtres")
print("   🛡️  Protection division par zéro activée")
print("   🕒 Timezone UTC configurée")

query_all = result.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .option("numRows", 20) \
    .option("checkpointLocation", "/tmp/checkpoint/all_transactions") \
    .trigger(processingTime='10 seconds') \
    .queryName("all_transactions") \
    .start()

print("🚨 Stream dédié aux anomalies détectées...")
query_anomalies = anomalies_only.select(
    "transaction_id", 
    "amount", 
    "z_score",
    "window"
).writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .option("checkpointLocation", "/tmp/checkpoint/anomalies_only") \
    .queryName("anomalies_only") \
    .trigger(processingTime='5 seconds') \
    .start()

print("⏳ Attente des flux de données...")
print("   💡 Le système calcule les z-scores par fenêtre de 1 minute")
print("   🎯 Seuil d'anomalie: z-score > 3.0")

# Attendre que les queries se terminent
query_all.awaitTermination()
