import mysql.connector
import schedule
from datetime import datetime
import time
from prettytable import PrettyTable

from webscraping.continente import get_continente
from webscraping.garrafeirasoares import get_garrafeira_soares
from webscraping.elingles import get_elingles
from webscraping.pvineyard import get_pvineyard
from webscraping.granvine import get_granvine
from webscraping.auchan import get_auchan

LastEANS = 0
NewEANS = 0
x = PrettyTable()
x.field_names = ["EAN", "Store Name",  "HarvestYear", "Price", "Discount", "Currency", "Date", "Location", "Link"]
sql_EAN_Query = "SELECT EAN FROM wines"
sql_NAME_Query = "SELECT Name FROM wines"
sql_insert_statement = """INSERT INTO scrape (EAN, StoreName, HarvestYear, Price, Discount, Currency, Date, Location, Link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

def count_eans(eans):
	count = 0
	for element in eans:
		if isinstance(element, list):
			count += count_eans(element)
		else:
			count += 1
	return count

def time_get():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	return current_time

def main():
	global LastEANS
	cursor.execute(sql_EAN_Query)
	eans = cursor.fetchall()
	cursor.execute(sql_NAME_Query)
	names = cursor.fetchall()
	
	y = -1
	for ean in eans:
		y = y + 1
		print("Scraping Wine \"" + str(names[y][0]) + "\"...")
		try:
			continente = get_continente(ean[0])
			x.add_row(continente)
			cursor.execute(sql_insert_statement, continente)
		except Exception as e:
			print(time_get() + ' Failed to scrape Continente')
			print("Message error: " + str(e))
			pass
		try:
			soares = get_garrafeira_soares(ean[0])
			x.add_row(soares)
			cursor.execute(sql_insert_statement, soares)
		except Exception as e:
			print(time_get() + ' Failed to scrape Garrafeira Soares')
			print("Message error: " + str(e))
			pass
		try:
			elingles = get_elingles(ean[0])
			x.add_row(elingles)
			cursor.execute(sql_insert_statement, elingles)
		except Exception as e:
			print(time_get() + ' Failed to scrape El Ingles')
			print("Message error: " + str(e))
			pass
		try:
			pvineyard = get_pvineyard(ean[0])
			x.add_row(pvineyard)
			cursor.execute(sql_insert_statement, pvineyard)
		except Exception as e:
			print(time_get() + ' Failed to scrape Portugal Vineyards')
			print("Message error: " + str(e))
			pass
		try:
			granvine = get_granvine(ean[0])
			x.add_row(granvine)
			cursor.execute(sql_insert_statement, granvine)
		except Exception as e:
			print(time_get() + ' Failed to scrape Granvine')
			print("Message error: " + str(e))
			pass
		try:
			auch = get_auchan(ean[0])
			x.add_row(auch)
			cursor.execute(sql_insert_statement, auch)
		except Exception as e:
			print(time_get() + ' Failed to scrape Granvine')
			print("Message error: " + str(e))
			pass
		print(x)
		x.clear_rows()
	print("Scrapping finished successfully!")
	conn.commit()
	print("Database upload completed!")
	print(time_get() + " - Finished Scrapping...")
	#cursor.close()
	#conn.close()

conn = mysql.connector.connect(host='34.175.219.22', database='wines', user='root', password='root')
cursor = conn.cursor()
print("Scraper started to run at " + time_get() + "...")
schedule.every(60).minutes.do(main)
while True:
	cursor.execute(sql_EAN_Query)
	eans = cursor.fetchall()
	LastEANS = count_eans(eans)

	time.sleep(5)
	cursor.execute(sql_EAN_Query)
	print(LastEANS)
	eans = cursor.fetchall()
	if NewEANS != LastEANS:
		main()
	NewEANS = count_eans(eans)
	print(NewEANS)
	schedule.run_pending()
