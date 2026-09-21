from pathlib import Path

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("dataframe")
    .master("local[*]")
    .getOrCreate()
)

csv_path = Path(__file__).resolve().parent.parent / "1_Resource" / "orders.csv"

df = spark.read.csv(str(csv_path), header=True, inferSchema=True)
df.show(5)

spark.stop()

# On Databricks, `spark` is created for you, so you only need:
#   df = spark.read.csv("/Volumes/development/data/files/orders/orders.csv", header=True)
#   df.show(5)
