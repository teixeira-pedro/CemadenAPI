from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import from_json,col, count

import json

schema_path = "schema.json"

with open(schema_path) as file:
    schema_data = json.load(file)
    bacias = StructType.fromJson(json.loads(schema_data))

## Iniciando sessao spark
spark = SparkSession.\
        builder\
        .appName('ConsumoTempoReal')\
        .getOrCreate()
## Lendo streaming
df = spark.readStream\
    .format("kafka")\
    .option("kafka.bootstrap.servers", "kafka:9093")\
    .option("subscribe", "topic-test")\
    .option("startingOffsets", "latest")\
    .load()
## Recebendo dados traduzidos
dados_bacia = df.select(col("value").cast("string").alias("value"))\
        .select(from_json(col("value"), bacias).alias("data"))\
        .select("data.*")

dados_bacia.printSchema()


def process_row(df, epoch_id):
    ## Selecionando a coluna concatenada para que a mesma cruze com fk.
    bacia_batch_selecionado = df.selectExpr("concat(x,'|',y) as fk")
    ## Verificando existencia de valores
    dados_presentes = bacia_batch_selecionado.count()
    ## Recolhendo fk
    fk = bacia_batch_selecionado.collect()[0] if dados_presentes > 0 else None
    ## Imprimindo fk
    print(fk)
    ## Se existir informacao
    ## Leia do banco de dados 
    # Read from SQL table
    if fk:
        busca = fk.__getitem__('fk')
        dados_pontos = spark.read.format("jdbc")\
        .option("driver","com.mysql.cj.jdbc.Driver")\
        .option("url", "jdbc:mysql://mydb:3306/ggvd")\
        .option("dbtable", f"(select * from locais_em_volta where fk = '{busca}')e")\
        .option("user", "root")\
        .option("password", "root")\
        .load()
        dados_pontos.show()

dados_bacia.writeStream\
   .foreachBatch(process_row)\
   .trigger(processingTime='45 seconds')\
   .start()\
   .awaitTermination()


# destination_workload = df1.writeStream\
#    .format("parquet")\
#    .outputMode("append")\
#    .option("path", "results/content")\
#    .trigger(processingTime='30 seconds')\
#    .option("checkpointLocation", "results/checkpoint")\
#    .start()