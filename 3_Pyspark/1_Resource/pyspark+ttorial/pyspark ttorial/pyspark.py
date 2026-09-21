# Databricks notebook source
# MAGIC %md
# MAGIC ### **create storage**

# COMMAND ----------

# DBTITLE 1,create db
# MAGIC %sql
# MAGIC CREATE DATABASE devlopment.data

# COMMAND ----------

# MAGIC %md
# MAGIC ### **create volumes**

# COMMAND ----------

# DBTITLE 1,cretat vol
# MAGIC %sql
# MAGIC CREATE VOLUME devlopment.data.files

# COMMAND ----------

# MAGIC %md
# MAGIC # **CREATE DATAFRAME**

# COMMAND ----------

df = spark.read.csv("/Volumes/devlopment/data/files/orders/orders.csv",header=True)
df.show()

# COMMAND ----------

display(df)

# COMMAND ----------

# DBTITLE 1,better way of creating df
df = spark.read.format("csv").option("header","True").option("inferSchema","True").load("/Volumes/devlopment/data/files/orders/orders.csv")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### **schema**

# COMMAND ----------

# DBTITLE 1,schema
df.printSchema()

# COMMAND ----------

# MAGIC %md
# MAGIC ### **READ JSON & PARQUET**

# COMMAND ----------

# DBTITLE 1,create data frame sing json
df = spark.read.json("/Volumes/devlopment/data/files/orders/order_json.json",multiLine=True)
display(df)

# COMMAND ----------

df=spark.read.format("json").option("multiLine","True").load("/Volumes/devlopment/data/files/orders/order_json.json")
display(df)

# COMMAND ----------

# DBTITLE 1,read parquet
df = spark.read.parquet("/Volumes/devlopment/data/files/orders/orders.parquet")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### **SELECT TRANSFORMATION**

# COMMAND ----------

df = spark.read.parquet("/Volumes/devlopment/data/files/orders/orders.parquet")
display(df)

# COMMAND ----------

display(df.select("order_id","customer_name","email"))

# COMMAND ----------

df.select(df.order_id,df.customer_name).show()

# COMMAND ----------

# DBTITLE 1,rename - alias
from pyspark.sql.functions import *
df.select(col("order_id"),col("customer_name").alias("cust_name")).show()


# COMMAND ----------

# MAGIC %md
# MAGIC ### **withColumn() & withColumnRenamed() in PySpark**

# COMMAND ----------

df = spark.read.parquet("/Volumes/devlopment/data/files/orders/orders.parquet")
display(df)

# COMMAND ----------

from pyspark.sql.functions import *
display(df.withColumn("id",col("order_id")+10))

# COMMAND ----------

display(df.withColumn("country",lit("USA")))

# COMMAND ----------

display(df.withColumn('order_id',col("order_id")+10))

# COMMAND ----------

display(df.withColumnRenamed("customer_name","name"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### **FILTER IN PYSPARK**

# COMMAND ----------

df = spark.read.parquet("/Volumes/devlopment/data/files/orders/orders.parquet")
display(df)

# COMMAND ----------

display(df.filter(df.status=='Done'))

# COMMAND ----------

display(df.filter(df.status!='Done'))

# COMMAND ----------

display(df.filter((df.payment_method=='Debit Card') & (df.status=='Completed')))

# COMMAND ----------

display(df.filter((df.payment_method=='Debit Card') | (df.status=='Completed')))

# COMMAND ----------

display(df.filter(df.email.startswith("a")))

# COMMAND ----------

display(df.filter(df.customer_name.endswith("n")))

# COMMAND ----------

display(df.filter(df.country.like("%Ind%")))

# COMMAND ----------

# MAGIC %md
# MAGIC ### **Difference Between dropDuplicates() vs distinct()**
# MAGIC
# MAGIC **distinct() → removes duplicate rows (entire row match).**
# MAGIC
# MAGIC **dropDuplicates([subset]) → removes duplicates based on one or more specific columns.**

# COMMAND ----------

data = [
    (1, "Alice", 23),
    (2, "Bob", 34),
    (3, "Charlie", 29),
    (1, "Alice", 23),   # duplicate row
    (2, "Bob", 34),     # duplicate row
    (6, "Alice", 30)    # same name, different age
]

columns = ["id", "name", "age"]

df = spark.createDataFrame(data, columns)
display(df)


# COMMAND ----------

display(df.distinct())

# COMMAND ----------

display(df.dropDuplicates())

# COMMAND ----------

display(df.dropDuplicates(['age']))

# COMMAND ----------

# MAGIC %md
# MAGIC ### **sort & orderBy**

# COMMAND ----------

df = spark.read.parquet("/Volumes/devlopment/data/files/orders/orders.parquet")
display(df)

# COMMAND ----------

display(df.sort('customer_name'))


# COMMAND ----------

display(df.orderBy('customer_name'))


# COMMAND ----------

display(df.sort(df.order_id.desc()))

# COMMAND ----------

display(df.sort(df.order_id.asc()))

# COMMAND ----------

# MAGIC %md
# MAGIC ### **What is groupBy() in PySpark?**
# MAGIC
# MAGIC **The groupBy() transformation groups rows that have the same values in specified column(s).**
# MAGIC
# MAGIC **After grouping, you must apply aggregation functions (like count, sum, avg, min, max).**
# MAGIC
# MAGIC **Similar to GROUP BY in SQL.**

# COMMAND ----------

data = [
    (1, "Alice", "NY", 2000),
    (2, "Bob", "CA", 1500),
    (3, "Charlie", "NY", 3000),
    (4, "David", "CA", 2500),
    (5, "Eve", "TX", 1800),
    (6, "Frank", "TX", 2200),
]

columns = ["id", "name", "state", "salary"]

df = spark.createDataFrame(data, columns)
display(df)


# COMMAND ----------

display(df.groupBy('state').count())

# COMMAND ----------

display(df.groupBy('state').agg({'salary':'sum'}))

# COMMAND ----------

display(df.groupBy('state').agg({'salary':'avg'}))

# COMMAND ----------

display(df.groupBy('state').agg({'salary':'max'}))

# COMMAND ----------

display(df.groupBy('state').agg({'salary':'min'}))

# COMMAND ----------

# MAGIC %md
# MAGIC ## **What is a Join in PySpark?**

# COMMAND ----------

# DBTITLE 1,emp df
emp_data = [
    (1, "Alice", 1),
    (2, "Bob", 2),
    (3, "Charlie", 3),
    (4, "David", 5)   # dept_id not in dept
]
emp_columns = ["emp_id", "name", "dept_id"]

emp_df = spark.createDataFrame(emp_data, emp_columns)
emp_df.show()


# COMMAND ----------

dept_data = [
    (1, "HR"),
    (2, "IT"),
    (3, "Finance"),
    (4, "Marketing")
]
dept_columns = ["dept_id", "dept_name"]

dept_df = spark.createDataFrame(dept_data, dept_columns)
dept_df.show()


# COMMAND ----------

# DBTITLE 1,inner
emp_df.join(dept_df,emp_df.dept_id==dept_df.dept_id,'inner').show()

# COMMAND ----------

emp_df.join(dept_df,emp_df.dept_id==dept_df.dept_id,'left').show()

# COMMAND ----------

# DBTITLE 1,right
emp_df.join(dept_df,emp_df.dept_id==dept_df.dept_id,'right').show()

# COMMAND ----------

# DBTITLE 1,fll outer join
emp_df.join(dept_df,emp_df.dept_id==dept_df.dept_id,'outer').show()

# COMMAND ----------

# DBTITLE 1,left_semi
emp_df.join(dept_df,emp_df.dept_id==dept_df.dept_id,'left_semi').show()

# COMMAND ----------

# DBTITLE 1,left_anti
emp_df.join(dept_df,emp_df.dept_id==dept_df.dept_id,'left_anti').show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## **What is union in PySpark?**
# MAGIC
# MAGIC **union() combines rows of two DataFrames into a single DataFrame.**
# MAGIC
# MAGIC **Like SQL UNION ALL → it keeps duplicates.**

# COMMAND ----------

data1 = [
    (1, "Alice", "HR"),
    (2, "Bob", "IT")
]
columns = ["id", "name", "dept"]

df1 = spark.createDataFrame(data1, columns)
df1.show()


# COMMAND ----------

data2 = [
    (3, "Charlie", "Finance"),
    (4, "David", "IT"),
    (2, "Bob", "IT")   # duplicate row
]

df2 = spark.createDataFrame(data2, columns)
df2.show()


# COMMAND ----------

df1.union(df2).show()

# COMMAND ----------

df1.union(df2).distinct().show()

# COMMAND ----------

# MAGIC %md
# MAGIC ### **What is fillna() in PySpark?**
# MAGIC
# MAGIC **Used to replace null (NaN) values in a DataFrame.**
# MAGIC
# MAGIC **Similar to SQL COALESCE or Pandas fillna().**
# MAGIC
# MAGIC **You can replace nulls with:**

# COMMAND ----------

df = spark.read.parquet("/Volumes/devlopment/data/files/orders/orders.parquet")
display(df)

# COMMAND ----------

display(df.na.fill(""))

# COMMAND ----------

display(df.na.fill(0))

# COMMAND ----------

display(df.fillna('UNKNOWN'))

# COMMAND ----------

display(df.na.fill("blank",["quantity"]))

# COMMAND ----------

display(df.na.fill("blank",["quantity"]).na.fill(0,["order_id"]))

# COMMAND ----------

# MAGIC %md
# MAGIC ## **StructType and StructField**
# MAGIC
# MAGIC ## **1. Definition**
# MAGIC
# MAGIC ### **StructType → Represents the entire schema of a DataFrame (like a container for all fields).**
# MAGIC
# MAGIC ### **StructField → Represents one single column/field inside that schema.**
# MAGIC
# MAGIC ### **StructType is like a list of StructField objects.**
# MAGIC
# MAGIC ### **StructField describes name, datatype, and nullability for one column.**

# COMMAND ----------

# DBTITLE 1,EXAMPLE
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Schema using StructType and StructField
schema = StructType([
    StructField("id", IntegerType(), False),
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

# Each StructField("colname", DataType, Nullable) = one column.

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import SparkSession

# Define schema
schema = StructType([
    StructField("id", IntegerType(), False),      # not nullable
    StructField("name", StringType(), True),      # nullable
    StructField("age", IntegerType(), True)       # nullable
])

# Sample data
data = [(1, "Alice", 30), (2, "Bob", 25), (3, None, 40)]

# Create DataFrame with schema
df = spark.createDataFrame(data, schema)

df.show()
df.printSchema()


# COMMAND ----------

# DBTITLE 1,IF YO HAVE CSV FILES THEN
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Define schema
schema = StructType([
    StructField("id", IntegerType(), False),      # not nullable
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True),
    StructField("salary", IntegerType(), True)
])

# Read CSV with schema
df = spark.read.csv("employees.csv", header=True, schema=schema)

df.printSchema()
df.show()


# COMMAND ----------

# MAGIC %md
# MAGIC ## **“pivot” and “unpivot”**
# MAGIC
# MAGIC ### **Pivot: turn row values into columns (wide format). Requires an aggregation.**
# MAGIC
# MAGIC ### **Unpivot: turn columns back into rows (long/tidy format). Spark doesn’t have a direct unpivot()**

# COMMAND ----------

data = [
    ("North","Laptop",10),
    ("North","Phone",20),
    ("South","Laptop",5),
    ("South","Phone",15),
    ("West","Laptop",7),
    ("West","Tablet",3)
]

columns = ["region","product","qty"]

df = spark.createDataFrame(data, columns)
df.show()


# COMMAND ----------

df.groupBy("region").pivot("product").sum("qty").show()

# COMMAND ----------

# DBTITLE 1,PIVOT
df1= df.groupBy("region").pivot("product").sum("qty")
df1.show()

# COMMAND ----------

# DBTITLE 1,UNPIVOT
from pyspark.sql.functions import expr
df1.select("region",expr("stack(3,'Laptop',Laptop,'Phone',Phone,'Tablet',Tablet) as (prodct,qty)")).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## **What is a UDF?**
# MAGIC
# MAGIC **A User Defined Function (UDF) lets you use custom Python logic inside Spark SQL/DataFrames.**
# MAGIC
# MAGIC **You register your Python function as a UDF so Spark can distribute it across the cluster.**
# MAGIC
# MAGIC **Use only if built-in Spark SQL functions can’t solve your problem (since UDFs can be slower).**

# COMMAND ----------

data = [
    ("Alice", "Delhi", 10),
    ("Bob", "Mumbai", 25),
    ("Charlie", "Bangalore", 60),
    ("David", "Pune", None)
]

columns = ["name", "city", "age"]

df = spark.createDataFrame(data, columns)
df.show()

# REQ - IF AGE IS NONE THEN UNKNOWN IF AGE<18 THEN MINOR ,18 <= age < 40 ADULT , IF AGE>40 THEN SENIOR  

# COMMAND ----------

def age_grp(age):
    if age is None:
        return "UNKNOWN"
    elif age < 18:
        return "MINOR"
    elif age >= 18 and age < 40:
        return "ADULT"
    else:
        return "SENIOR"
age_grp(10)

# COMMAND ----------

from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

age_grp_category= udf(age_grp,StringType())

# COMMAND ----------

df.withColumn('age_cat',age_grp_category(df.age)).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## **createOrReplaceTempView**
# MAGIC
# MAGIC **It creates a temporary SQL view from a DataFrame.**
# MAGIC
# MAGIC **The view exists only for the Spark session (not permanent in the metastore).**
# MAGIC
# MAGIC **You can run SQL queries directly on it.**

# COMMAND ----------

data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
columns = ["name", "age"]

df = spark.createDataFrame(data, columns)
df.show()



# COMMAND ----------

df.createOrReplaceTempView("test")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from test

# COMMAND ----------

df = spark.read.parquet("/Volumes/devlopment/data/files/orders/orders.parquet")
df.createOrReplaceTempView('orders')

# COMMAND ----------

# MAGIC %sql 
# MAGIC select count(distinct order_id),min(order_date) from orders

# COMMAND ----------

# MAGIC %md
# MAGIC ## **Window Functions in PySpark**
# MAGIC **ROW_NUMBER, RANK, DENSE_RANK, LAG, and LEAD.**

# COMMAND ----------


data = [
    ("Amit",   "Sales", 5000),
    ("Ravi",   "Sales", 4800),
    ("Neha",   "Sales", 4800),
    ("Suman",  "Sales", 4700),
    ("Kiran",  "Sales", 4700),
    ("Meena",  "Sales", 4700),
    ("Raj",    "Sales", 4600),
    ("Pooja",  "HR",    5200),
    ("Anil",   "HR",    5100),
    ("Ramesh", "HR",    5100),
    ("Seema",  "HR",    5000),
    ("Vikas",  "HR",    5000),
    ("Priya",  "HR",    4800),
    ("Nisha",  "HR",    4800),
    ("Arun",   "HR",    4700)
]

columns = ["name", "dept", "salary"]

df = spark.createDataFrame(data, columns)
df.show()


# COMMAND ----------

df.createOrReplaceTempView("employee")

# COMMAND ----------

# MAGIC %sql
# MAGIC select *, row_number() over(partition by dept order by salary desc) rn from employee

# COMMAND ----------

# MAGIC %md
# MAGIC **ROW_NUMBER()**
# MAGIC
# MAGIC 👉 Assigns a unique sequential number to each row within a partition (group), ordered by a column.
# MAGIC
# MAGIC Even if values are the same, each row gets a different number.
# MAGIC ✅ Example: 1,2,3,4…

# COMMAND ----------

# DBTITLE 1,row number
from pyspark.sql.window import Window
from pyspark.sql.functions import *

w = Window.partitionBy('dept').orderBy(col('salary').desc())
df.withColumn('rn',row_number().over(w)).show()



# COMMAND ----------

# MAGIC %md
# MAGIC **RANK()**
# MAGIC
# MAGIC 👉 Assigns a rank to rows within a partition based on order.
# MAGIC
# MAGIC Ties get the same rank.
# MAGIC
# MAGIC But the next rank will skip numbers.
# MAGIC ✅ Example: 1, 2, 2, 4 (notice skip of 3).

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import *

w = Window.partitionBy('dept').orderBy(col('salary').desc())
df.withColumn('rn',rank().over(w)).show()



# COMMAND ----------

# MAGIC %md
# MAGIC **DENSE_RANK()**
# MAGIC
# MAGIC 👉 Similar to RANK, but it does not skip numbers after ties.
# MAGIC
# MAGIC Ties get the same rank.
# MAGIC
# MAGIC Next rank is consecutive.
# MAGIC ✅ Example: 1, 2, 2, 3 (no skip).

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import *

w = Window.partitionBy('dept').orderBy(col('salary').desc())
df.withColumn('rn',dense_rank().over(w)).show()



# COMMAND ----------

# MAGIC %md
# MAGIC **LAG(column, n)**
# MAGIC
# MAGIC 👉 Fetches the value from the previous row (n steps back) in the same partition.
# MAGIC
# MAGIC Useful for comparing with “previous record”.
# MAGIC ✅ Example: Salary difference from last employee.

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import *

w = Window.partitionBy('dept').orderBy(col('salary').desc())
df.withColumn('rn',lag(col('salary'),1).over(w)).show()



# COMMAND ----------

# MAGIC %md
# MAGIC **LEAD(column, n)**
# MAGIC
# MAGIC 👉 Fetches the value from the next row (n steps ahead) in the same partition.
# MAGIC
# MAGIC Useful for comparing with “next record”.
# MAGIC ✅ Example: Salary gap with next higher salary.

# COMMAND ----------

from pyspark.sql.window import Window
from pyspark.sql.functions import *

w = Window.partitionBy('dept').orderBy(col('salary').desc())
df.withColumn('rn',lead(col('salary'),1).over(w)).show()



# COMMAND ----------

# MAGIC %md
# MAGIC ## **partitionBy AND repartition in PySpark**

# COMMAND ----------

from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.getOrCreate()

# ---------- 1) Build a larger DataFrame (no RDD usage) ----------
categories = ["Electronics","Grocery","Clothing","Home","Sports"]
regions    = ["North","South","East","West","Central"]
years      = [2023, 2024, 2025]
months     = list(range(1, 13))

df_cat   = spark.createDataFrame([(c,) for c in categories], ["category"])
df_reg   = spark.createDataFrame([(r,) for r in regions],    ["region"])
df_year  = spark.createDataFrame([(y,) for y in years],      ["year"])
df_month = spark.createDataFrame([(m,) for m in months],     ["month"])

# ~ 5*5*3*12 = 900 key rows before expanding to transactions
grid = df_cat.crossJoin(df_reg).crossJoin(df_year).crossJoin(df_month)

# Expand each key-row to 5..20 transactions using explode(sequence(1, n))
df = (
    grid
    .withColumn("n", F.floor(F.rand(seed=42) * 16 + 5))  # 5..20
    .select(
        "*",
        F.explode(F.sequence(F.lit(1), F.col("n"))).alias("txn_id")
    )
    .drop("n")
    .withColumn("sales", (F.rand(seed=7) * 900 + 100).cast("int"))   # 100..1000
    .withColumn("units", (F.rand(seed=11) * 9 + 1).cast("int"))      # 1..10
    .withColumn(
        "dt",
        F.to_date(F.concat_ws("-", F.col("year"), F.col("month"), F.lit(1)))
    )
)

print("Row count:", df.count())
display(df)

# COMMAND ----------

df.write.mode('overwrite').partitionBy("region").parquet("/Volumes/devlopment/data/files/sales")

# COMMAND ----------

df.repartition(3).write.mode('overwrite').partitionBy("region").parquet("/Volumes/devlopment/data/files/sales1/")


# COMMAND ----------

df.coalesce(1).write.mode('overwrite').partitionBy("region").parquet("/Volumes/devlopment/data/files/sales1/")


# COMMAND ----------

# MAGIC %md
# MAGIC ## **DATE FORMAT IN PYSAPRK **

# COMMAND ----------

from pyspark.sql import SparkSession, functions as F


data = [
    (1, "2025-08-23"),
    (2, "2025-12-05"),
    (3, "2024-01-01"),
    (4, "2023-07-15")
]

df = spark.createDataFrame(data, ["id", "date"])
display(df)

2025-08-23  --- 2025/12/05


# COMMAND ----------

from pyspark.sql.functions import *
df.select("id","date",date_format("date","yyyy/MM/dd")).show()

# COMMAND ----------

from pyspark.sql.functions import *
df.select("id","date",date_format("date","yyyy/MMMM/dd")).show()

# COMMAND ----------

from pyspark.sql.functions import *
df.select("id","date",date_format("date","dd/MM/yyyy")).show()

# COMMAND ----------

from pyspark.sql.functions import *
df.select("id","date",date_format("date","dd-MMM-yyyy")).show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## **DIFFERENT DATE FUNCTIONS**

# COMMAND ----------

from pyspark.sql import SparkSession, functions as F


data = [
    (1, "2025-08-23"),
    (2, "2025-12-05"),
    (3, "2024-01-01"),
    (4, "2023-07-15")
]

df = spark.createDataFrame(data, ["id", "date"])
display(df)



# COMMAND ----------

from pyspark.sql.functions import *
df.select('id',"date",date_add("date",6)).show()

# COMMAND ----------

from pyspark.sql.functions import *
df1=df.select('id',"date",date_sub("date",6).alias("new_date"))

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

df1.show()

# COMMAND ----------

df1.select("date","new_date",datediff("date","new_date")).show()

# COMMAND ----------

df1.select("date",add_months("date",1)).show()

# COMMAND ----------

df1.select("date",current_date()).show()

# COMMAND ----------

df1.select("date",current_date(),last_day("date")).show()

# COMMAND ----------

df1.select("date",current_date(),last_day("date"),next_day("date","monday")).show()

# COMMAND ----------

df1.select(current_date(),year(current_date())).show()

# COMMAND ----------

df1.select(current_date(),quarter(current_date())).show()

# COMMAND ----------

# MAGIC %md
# MAGIC **What is explode?**
# MAGIC
# MAGIC In PySpark, explode() is used to transform an array or map column into multiple rows.

# COMMAND ----------


data = [
    (1, ["apple", "banana", "orange"]),
    (2, ["grapes", "melon"]),
    (3, [])
]
df = spark.createDataFrame(data, ["id", "fruits"])
display(df)


# COMMAND ----------

# DBTITLE 1,explode()
from pyspark.sql.functions import *
df.select("id",explode("fruits")).show()

# COMMAND ----------

# DBTITLE 1,posexplode()
from pyspark.sql.functions import *
df.select("id",posexplode("fruits")).show()

# COMMAND ----------

# DBTITLE 1,EXPLODE MAP COLMNS
data = [
    (1, {"math": 90, "english": 85}),
    (2, {"math": 70, "science": 80})
]
df = spark.createDataFrame(data, ["id", "scores"])
display(df)

# COMMAND ----------

df.select("id",explode("scores")).show()

# COMMAND ----------

