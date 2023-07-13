from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import from_json,col, count, date_format, to_timestamp, lpad, year, month, dayofmonth

import json

schema_path = "/opt/spark-apps/schema.json"

with open(schema_path) as file:
    schema_data = json.load(file)
    estacaos = StructType.fromJson(json.loads(schema_data))

## Iniciando sessao spark
spark = SparkSession.\
        builder\
        .appName('ConsumoTempoReal')\
        .getOrCreate()
## Lendo streaming
df = spark.readStream\
    .format("kafka")\
    .option("failOnDataLoss", "false")\
    .option("kafka.bootstrap.servers", "kafka:9093")\
    .option("subscribe", "topic-test")\
    .option("startingOffsets", "latest")\
    .load()
## Recebendo dados traduzidos
dados_estacao = df.select(col("value").cast("string").alias("value"))\
        .select(from_json(col("value"), estacaos).alias("data"))\
        .select("data.*")

dados_estacao.printSchema()


def processar_informacao_estacao_advinda(df, epoch_id):
    ## Selecionando a coluna concatenada para que a mesma cruze com fk.
    estacao_batch_selecionado = df.selectExpr("pk as fk")
    ## Selecionando dado reserva com todas as colunas
    estacao_batch_todas_as_colunas = df.selectExpr("*")
    ## Verificando existencia de valores
    dados_presentes = estacao_batch_selecionado.count()
    ## Recolhendo fk
    fk = estacao_batch_selecionado.collect()[0] if dados_presentes > 0 else None
    ## Imprimindo fk
    print(fk)
    ## Se existir informacao
    ## Leia do banco de dados 
    # Read from SQL table
    if fk:
        busca = fk.__getitem__('fk')
        print("REALIZANDO CONSULTA: \n")
        print(f"(select * from locais_em_volta where fk = '{busca}')e")
        dados_pontos = spark.read.format("jdbc")\
        .option("driver","com.mysql.cj.jdbc.Driver")\
        .option("url", "jdbc:mysql://mydb:3306/ggvd")\
        .option("dbtable", f"(select * from locais_em_volta where fk = '{busca}')e")\
        .option("user", "dev")\
        .option("password", "dev")\
        .load()
        if dados_pontos.count() > 0:
            ## Juncao informacao estacao com locais afetados
            dados_estacao_data_formatada = estacao_batch_todas_as_colunas.withColumn("datahoraocc", to_timestamp(col("dht"), "yyyy-MM-dd'T'HH:mm:ss"))
            ## Realizando consulta de juncao
            dados_estacao_data_formatada = dados_estacao_data_formatada.withColumnRenamed("pk", "estacao_pk")
            dados_pontos_com_dados_estacao = dados_estacao_data_formatada.join(dados_pontos, dados_estacao_data_formatada.estacao_pk == dados_pontos.fk, "inner") 
            ## Realizando criacao de particoes
            dados_pontos_com_dados_estacao_particionados = dados_pontos_com_dados_estacao.withColumn("ano",       year(col("datahoraocc")).cast("string"))\
                                                                                         .withColumn("anomes",     lpad(month(col("datahoraocc")).cast("string"), 2, '0'))\
                                                                                         .withColumn("anomesdia", lpad(dayofmonth(col("datahoraocc")).cast("string"), 2, '0'))
            dados_pontos_com_dados_estacao_particionados.write\
               .option("maxRecordsPerFile", 1000)\
               .partitionBy("ano", "anomes", "anomesdia")\
               .mode("append")\
               .parquet("batch_resultados/")
            print("Dados processados com sucesso.")
            ## Retornando informacoes de juncao
            return dados_pontos_com_dados_estacao_particionados
        else:
            print("Dados vazios, prosseguindo.")

        
## Controle de streaming
## Configuracao de output em formato parquet
## Configuracao de saida para resultados e conteudo 
## Configuracao de checkpoint em caso de tolerância a falha
## Configuracao de janela em 45 segundos de atraso
## Modo append para nao sobrescrever os resultados anteriores e manter historico
## Salvando dados partitionados de modo a fica mais facil para localiza-los posteriormente
dados_estacao.writeStream\
   .foreachBatch(processar_informacao_estacao_advinda)\
   .trigger(processingTime='45 seconds')\
   .start()\
   .awaitTermination()

# .format("parquet")\

#    .option("path", "resultados/conteudo")\
#    .option("checkpointLocation", "resultados/checkpoint")\

#    .partitionBy("ano", "anomes", "anomesdia")\