import mysql.connector
from webscraping.continente import get_continente
from webscraping.garrafeirasoares import get_garrafeira_soares

ean = input('EAN: ')

conn = mysql.connector.connect(host='34.175.219.22', database='wines', user='root', password='root')
cursor = conn.cursor()
sql_create_table_statement = """CREATE TABLE pls (
  name VARCHAR(255) NULL,
  PRIMARY KEY (name))"""
sql_insert_statement = """INSERT INTO pls (name) VALUES (%s)"""
#cursor.execute(sql_create_table_statement)
cursor.execute(sql_insert_statement, [ean])
conn.commit()
cursor.close()
conn.close()
print(ean)
get_continente(ean)
get_garrafeira_soares(ean)