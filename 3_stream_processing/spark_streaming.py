"""
Spark Structured Streaming - Stock Market Analytics (dengan 5 saham)
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_json, to_timestamp, from_unixtime,
    window, avg, max as spark_max, min as spark_min, sum as spark_sum, count
)
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, LongType
)


KAFKA_BROKER = "localhost:9093"
KAFKA_TOPIC = "stock-prices-tl"

POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "6797"
POSTGRES_DB = "stock_db"

POSTGRES_URL = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


STOCK_SCHEMA = StructType([
    StructField("symbol", StringType(), True),
    StructField("name", StringType(), True),
    StructField("exchange", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("open", DoubleType(), True),
    StructField("high", DoubleType(), True),
    StructField("low", DoubleType(), True),
    StructField("volume", LongType(), True),
    StructField("timestamp", LongType(), True),
    StructField("source", StringType(), True),
    StructField("fetched_at", StringType(), True),
])


def create_spark_session():
    return SparkSession.builder \
        .appName("StockMarketStreamingTL") \
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
            "org.postgresql:postgresql:42.7.3"
        ) \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.streaming.stopGracefullyOnShutdown", "true") \
        .master("local[*]") \
        .getOrCreate()


def read_kafka_stream(spark):
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()


def parse_and_clean(kafka_df):
    parsed = kafka_df \
        .selectExpr("CAST(value AS STRING) AS json_str") \
        .select(from_json(col("json_str"), STOCK_SCHEMA).alias("data")) \
        .select("data.*")

    cleaned = parsed \
        .filter(col("price").isNotNull() & (col("price") > 0)) \
        .filter(col("symbol").isNotNull())

    transformed = cleaned \
        .withColumn("event_time", to_timestamp(from_unixtime(col("timestamp") / 1000))) \
        .withColumn("fetched_at_ts", to_timestamp(col("fetched_at")))

    return transformed


def write_to_postgres(table_name, mode="append"):
    def foreach_batch_function(batch_df, epoch_id):
        try:
            batch_df.write \
                .format("jdbc") \
                .option("url", POSTGRES_URL) \
                .option("dbtable", table_name) \
                .option("user", POSTGRES_USER) \
                .option("password", POSTGRES_PASSWORD) \
                .option("driver", "org.postgresql.Driver") \
                .mode(mode) \
                .save()
            print(f"[OK] Epoch {epoch_id}: Berhasil tulis {batch_df.count()} baris ke {table_name}")
        except Exception as e:
            print(f"[ERROR] Epoch {epoch_id}: Gagal tulis ke {table_name}: {e}")

    return foreach_batch_function


def main():
    print("=" * 70)
    print("SPARK STRUCTURED STREAMING - Stock Market Analytics")
    print("=" * 70)
    print(f"Kafka Broker : {KAFKA_BROKER}")
    print(f"Kafka Topic  : {KAFKA_TOPIC}")
    print(f"PostgreSQL   : {POSTGRES_URL}")
    print("=" * 70)

    print("\n[INIT] Membuat SparkSession...")
    spark = create_spark_session()
    spark.sparkContext.setLogLevel("WARN")
    print("[OK] SparkSession dibuat")

    print("[INIT] Membaca stream dari Kafka...")
    kafka_df = read_kafka_stream(spark)

    print("[INIT] Parse JSON & Data Cleaning...")
    cleaned_df = parse_and_clean(kafka_df)

    print("[INIT] Setup query 1: stock_prices (raw data)...")
    query_raw = cleaned_df \
        .select(
            "symbol", "name", "exchange",
            "price", "open", "high", "low", "volume",
            col("timestamp").alias("event_timestamp"),
            "source",
            col("fetched_at_ts").alias("fetched_at")
        ) \
        .writeStream \
        .foreachBatch(write_to_postgres("stock_prices")) \
        .outputMode("append") \
        .option("checkpointLocation", "C:/Users/jacin/Documents/Streaming_AnalyticsSahamTL/checkpoint/raw") \
        .start()

    print("[INIT] Setup query 2: stock_trends (aggregated)...")
    aggregated_df = cleaned_df \
        .withWatermark("event_time", "30 seconds") \
        .groupBy(
            window(col("event_time"), "1 minute"),
            col("symbol")
        ) \
        .agg(
            avg("price").alias("avg_price"),
            spark_max("high").alias("max_price"),
            spark_min("low").alias("min_price"),
            spark_sum("volume").alias("total_volume"),
            count("*").alias("data_points")
        ) \
        .select(
            col("symbol"),
            col("window.start").alias("window_start"),
            col("window.end").alias("window_end"),
            "avg_price", "max_price", "min_price",
            "total_volume", "data_points"
        )

    query_agg = aggregated_df \
        .writeStream \
        .foreachBatch(write_to_postgres("stock_trends")) \
        .outputMode("update") \
        .start()

    print("\n" + "=" * 70)
    print("[RUNNING] Spark Streaming aktif. Menunggu data dari Kafka...")
    print("Tekan Ctrl+C untuk berhenti.")
    print("=" * 70 + "\n")

    try:
        spark.streams.awaitAnyTermination()
    except KeyboardInterrupt:
        print("\n[STOP] Dihentikan oleh user")
        query_raw.stop()
        query_agg.stop()
        spark.stop()
        print("[OK] Spark Streaming dihentikan")


if __name__ == "__main__":
    main()