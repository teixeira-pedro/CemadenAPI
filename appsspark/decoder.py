from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import json
from pyspark.sql.types import StructType, StringType

spark = SparkSession.\
        builder\
        .appName('Decodificador')\
        .getOrCreate()

df = spark.read.json("data.json", multiLine=True)
string_schema = df.schema.json()

with open("schema.json", 'w') as file:
        json.dump(string_schema, file)

with open("schema.json", 'r') as file:
        sch = json.load(file)
        schema = StructType.fromJson(json.loads(sch))
        print(schema)
