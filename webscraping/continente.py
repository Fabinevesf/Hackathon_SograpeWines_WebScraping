from webscraping.continente_cookie import get_continente_cookie
from bs4 import BeautifulSoup
import requests
import time

def get_continente(ean):
	html = get_continente_cookie(ean)
	soup = BeautifulSoup(html, "html.parser")

	total = soup.find_all('span', class_='ct-price-formatted')[0].text
	total = total.replace('\n', '')
	currency = total[0]
	price = total[1::1]
	discount = 0

	name = soup.find_all('h1', class_='product-name')[0].text
	name = name.replace("\n", "")

	capacity = (soup.find_all('span', class_='ct-pdp--unit col-pdp--unit'))[0].text
	bottle_size = capacity.split(" ")[1]
	if "cl" in capacity:
		if "," in capacity:
			bottle_size = bottle_size.replace(',', '')
		else:
			bottle_size = bottle_size + "0"
	if "lt" in capacity:
		bottle_size = bottle_size.replace(',', '')
		bottle_size = bottle_size + "00"

	origem = (soup.find_all('p', class_='mb-20'))[2].text
	origem = origem.replace('\n', '')
	cur_time = time.asctime(time.localtime())
	
	try:
		discount = (soup.find_all('div', class_='ct-product-tile-badge-value-wrapper col-product-tile-badge-value-wrapper ct-product-tile-badge-value-wrapper--pvpr col-product-tile-badge-value-wrapper--pvpr   '))[0].text
		print(discount)
		discount = 1
	except:
		discount = 0	

	print(ean)
	print(name)
	print(price)
	print(discount)
	print(currency)
	print(cur_time)
	print(origem)

	return[ean, "Continente", None, float(price), discount, currency, cur_time, origem]