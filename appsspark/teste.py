from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import json
from pyspark.sql.types import StructType, StringType

spark = SparkSession.\
        builder\
        .appName('Testador')\
        .getOrCreate()

df = spark.read.parquet("./resultados/conteudo/ano=__HIVE_DEFAULT_PARTITION__/anomes=__HIVE_DEFAULT_PARTITION__/anomesdia=__HIVE_DEFAULT_PARTITION__/part-00000-53ec5472-2077-4211-bf89-5ffe9420a8dd.c000.snappy.parquet")
df.show(truncate=False)