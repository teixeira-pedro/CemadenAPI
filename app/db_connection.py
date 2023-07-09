import mysql.connector
from sqlalchemy import create_engine

engine =  create_engine('mysql+pymysql://root:root@mydb/ggvd')
mydb = mysql.connector.connect(
  host="mydb",
  user="root",
  password="root",
  port=3306,
  database='ggvd'
)

print(mydb)