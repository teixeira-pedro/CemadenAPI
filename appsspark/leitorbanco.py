from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import json
from pyspark.sql.types import StructType, StringType

spark = SparkSession.\
        builder\
        .appName('LeitorBanco')\
        .getOrCreate()

# Read from SQL table
df = spark.read.format("jdbc")\
  .option("driver","com.mysql.cj.jdbc.Driver")\
  .option("url", "jdbc:mysql://mydb:3306/ggvd")\
  .option("dbtable", "(select * from locais_em_volta)e")\
  .option("user", "root")\
  .option("password", "root")\
  .load()

df.show()