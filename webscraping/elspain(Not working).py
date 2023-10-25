import requests
import re
from bs4 import BeautifulSoup
import datetime
import time

#NOME ANO CAPACIDADE EAN WEBSITE LINK PREÇO MOEDA LOCALIZAÇÃO

def get_elspain(ean):
	url = "https://www.elcorteingles.es/supermercado/buscar/?term=" + str(ean)

	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	product_link = soup.find_all('a', class_='js-product-link')[0]['href']
	product_link = "https://www.elcorteingles.es" + product_link

	response = requests.get(product_link, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	name = soup.find_all('div', class_='pdp-title mb')[0].text.replace('\n', ' ')
	name = name.split(" garrafa")[0]
	if (name.endswith(" ")):
		name = name[:-1]

	try:
		discount = soup.find_all('div', class_='prices-price _before')[0].text
		discount = 1
		price = soup.find_all('div', class_='prices-price _offer')[0].text
		currency = price.split(" ")[1]
		price = price.split(" ")[0].replace(',', '.')
		price = float(price)
	except:
		discount = 0
		price = soup.find('div', class_='prices-price _current')
		price = price.get_text(strip=True)
		currency = price.split(" ")[1]
		price = price.split(" ")[0].replace(',', '.')
		price = float(price)

	capacity = soup.find_all('span', class_='info-key')
	for i in capacity:
		if (i.text == "Cantidad Neta:"):
			capacity = i.next_sibling.text.strip(' ')
			if "Centilitros" in capacity:
				capacity = capacity.split(" ")[0] + "0 ml"
			if "Mililitros" in capacity:
				capacity = capacity.split(" ")[0] + " ml"
			if "Litros" in capacity:
				capacity = capacity.split(" ")[0]
				capacity = float(capacity) * 1000
			break

	website = "elcorteingles"

	img = soup.find_all('img', class_='js-zoom-to-modal-image')[0]['src']
	img = "https:" + img

	print("wat")
	print("Name: " + name)
	print("Ano: " + str(None))
	print("Capacidade: " + capacity)
	print("EAN: " + str(ean))
	print("Website: " + website)
	print("Link: " + product_link)
	print("Price: ", price)
	print("Discount: " + str(discount) + "%")
	print("Currency: " + currency)
	print("Localização: " + str(None))
	print("Imagem: " + img)
	date = datetime.datetime.now()
	#return [str(ean), "El Corte Ingles", "0", str(price), str(discount), str(currency), str(date), "Spain"]

get_elspain(5601012011500)
