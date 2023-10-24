import mysql.connector
from webscraping.continente import get_continente
from webscraping.garrafeirasoares import get_garrafeira_soares
from webscraping.elingles import get_elingles

ean = input('EAN: ')

conn = mysql.connector.connect(host='34.175.219.22', database='wines', user='root', password='root')
cursor = conn.cursor()
sql_create_table_statement = """CREATE TABLE data (
  id INT NOT NULL AUTO_INCREMENT,
  date_time DATETIME NOT NULL,
  name VARCHAR(255) NOT NULL,
  price VARCHAR(255) NOT NULL,
  capacidade VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);"""
sql_insert_statement = """INSERT INTO data (date_time, name, price, capacidade) VALUES (%s, %s, %s, %s)"""
#cursor.execute(sql_create_table_statement)
print(ean)
print("--------------------------------------------")
get_continente(ean)
print("--------------------------------------------")
soares = get_garrafeira_soares(ean)
print("--------------------------------------------")
cursor.execute(sql_insert_statement, soares)
get_elingles(ean)
print("--------------------------------------------")
conn.commit()
cursor.close()
conn.close()