from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, IntegerType, StringType, StructField, StructType
from pathlib import Path

spark = (
    SparkSession.builder
    .appName("DataWar_First_Spark_Job")
    .master("local[2]")
    .getOrCreate()
)

data_dir = Path(__file__).resolve().parent.parent / "1_Resource"
orders_path = data_dir / "orders.csv"

schema = StructType([
    StructField("order_id", DoubleType(), True),
    StructField("customer_name", StringType(), True),
    StructField("email", StringType(), True),
    StructField("order_date", StringType(), True),
    StructField("product", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", DoubleType(), True),
    StructField("payment_method", StringType(), True),
    StructField("status", StringType(), True),
    StructField("shipping_address", StringType(), True),
    StructField("country", StringType(), True),
    StructField("delivery_date", StringType(), True),
])

orders = spark.read.option("header", True).schema(schema).csv(str(orders_path))

print(f"Total rows   : {orders.count()}")
print(f"Spark version: {spark.version}")

orders.groupBy("country").count().orderBy("count", ascending=False).show(10, truncate=False)

orders.groupBy("product").count().orderBy("count", ascending=False).show(10, truncate=False)

spark.stop()
print("First Spark job finished successfully.")