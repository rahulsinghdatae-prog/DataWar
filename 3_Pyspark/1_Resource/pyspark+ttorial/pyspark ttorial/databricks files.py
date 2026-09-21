# Databricks notebook source
import common
common.url

# COMMAND ----------

common.region

# COMMAND ----------

common.geo

# COMMAND ----------

with open("/Workspace/Users/manish666tiwari@gmail.com/pyspark ttorial/common.txt","r") as f:
  print(f.read())

# COMMAND ----------

with open("/Workspace/Users/manish666tiwari@gmail.com/pyspark ttorial/common1.txt","w") as f:
    f.write("hello world")

# COMMAND ----------

