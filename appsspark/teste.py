from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import json
from pyspark.sql.types import StructType, StringType

spark = SparkSession.\
        builder\
        .appName('Testador')\
        .getOrCreate()

df = spark.read.parquet("./batch_resultados/")
df.show(truncate=False)