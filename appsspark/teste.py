from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import json
from pyspark.sql.types import StructType, StringType

spark = SparkSession.\
        builder\
        .appName('Testador')\
        .getOrCreate()

df = spark.read.parquet("/opt/spark-apps/batch_resultados/")
df = df.withColumn("nivel", F.when(F.col("status_rio").contains("SUBINDO"), 1)\
                             .when(F.col("status_rio").contains("ESTAVEL"), 0)\
                             .when(F.col("status_rio").contains("DESCEDO"), 2)\
                             .otherwise(-1))
# df.select("nivel").distinct().show(truncate=False)
df.createOrReplaceTempView("geral")

print("\nESTACOES COM NUMERO DE LOCAIS AFETADOS ONDE O NIVEL DO RIO ESTA SUBINDO:\n")
spark.sql('''
SELECT estacao_pk, dht, count(endereco) as `locais afetados`
 FROM geral 
 WHERE nivel = 1
 GROUP BY estacao_pk, dht
''').show(truncate=False)

print("ESTACOES COM LOCAIS ONDE O STATUS DA ESTACAO ESTA COMO VIGILANCIA:\n")
spark.sql('''
SELECT estacao_pk, dht, count(endereco) as `locais_vigilancia`
FROM geral
WHERE status = 'VIGILÂNCIA'
GROUP BY estacao_pk, dht
''').show(truncate=False)

print("ESTACOES QUE REPORTARAM RIOS COM NIVEL ESTAVEL EM NITEROI\n")
df = df.withColumn('endereco', F.split(F.col("endereco"), ', ').alias('endereco'))
df.createOrReplaceTempView("geralSplit")
spark.sql('''
SELECT distinct(estacao_pk) as `estacoes_nivel_estavel_niteroi`
 FROM geralSplit
 WHERE endereco[4] = 'Niterói' or endereco[3] = 'Niterói'
   and nivel = 0 
''').show(truncate=False)



