import mysql.connector
from webscraping.continente import get_continente
from webscraping.garrafeirasoares import get_garrafeira_soares
from webscraping.elingles import get_elingles

conn = mysql.connector.connect(host='34.175.219.22', database='wines', user='root', password='root')
cursor = conn.cursor()
sql_select_Query = "SELECT EAN FROM wines"
sql_insert_statement = """INSERT INTO scrape (EAN, StoreName, HarvestYear, Price, Discount, Currency, Date, Location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
cursor.execute(sql_select_Query)

eans = cursor.fetchall()
print(eans)
for ean in eans:
  print("--------------------------------------------")
  continente = get_continente(ean[0])
  cursor.execute(sql_insert_statement, continente)
  print("--------------------------------------------")
  soares = get_garrafeira_soares(ean[0])
  print("--------------------------------------------")
  elingles = get_elingles(ean[0])
  cursor.execute(sql_insert_statement, elingles)
  print("--------------------------------------------")
conn.commit()
cursor.close()
conn.close()
