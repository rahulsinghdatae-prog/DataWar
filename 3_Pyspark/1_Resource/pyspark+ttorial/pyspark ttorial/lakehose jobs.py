# Databricks notebook source
df = spark.read.csv("/Volumes/devlopment/lake/lake_practical/sales/",header=True)
display(df)

# COMMAND ----------

from pyspark.sql.functions import to_date,col
df_clean = (df.withColumn("order_date", to_date(col("order_date"), "yyyy-MM-dd"))
              .withColumn("amount", col("amount").cast("decimal(12,2)"))
              .dropna(subset=["order_id","amount"]))

# Write to Silver Delta Table
(df_clean.write.format("delta")
         .mode("overwrite")
         .saveAsTable("devlopment.lake.sales_orders"))

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from devlopment.lake.sales_orders

# COMMAND ----------

