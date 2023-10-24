import requests
from bs4 import BeautifulSoup

def get_continente(ean):
	url = "https://www.continente.pt/pesquisa/?q="
	url = url + ean
	response = requests.get(url, cookies={'dwsid':'LT_YtM8_xZLDvEwyRBXjSC6dy1q8yJAAIp0NZvBa_9lRBvwesJi5jtM6UMA741GwX70rTTcG3nFyUSyBS6pH3Q=='}, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})

	soup = BeautifulSoup(response.content, "html.parser")

	product = soup.find_all('div', class_='ct-image-container')[0]

	product_link = product.find_all('a')[0]['href']

	response = requests.get(product_link, cookies={'dwsid':'LT_YtM8_xZLDvEwyRBXjSC6dy1q8yJAAIp0NZvBa_9lRBvwesJi5jtM6UMA741GwX70rTTcG3nFyUSyBS6pH3Q=='})

	soup = BeautifulSoup(response.content, "html.parser")

	total = soup.find_all('span', class_='ct-price-formatted')[0].text
	total = total.replace('\n', '')
	currency = total[0]
	price = total[1::1]

	name = soup.find_all('h1', class_='product-name')[0].text
	name = name.replace("\n", "")

	capacity = (soup.find_all('span', class_='ct-pdp--unit col-pdp--unit'))[0].text
	capacity = capacity.replace("garrafa ", "")
	capacity = capacity.replace("\n", "")
	if "cl" in capacity:
		capacity = capacity.replace(" cl", "")
		capacity = capacity + "0"

	origem = (soup.find_all('p', class_='mb-20'))[2].text
	origem = origem.replace('\n', '')

	print("Name: " + name)
	print("Ano: " + str(None))
	print("Capacidade (em ML): " + capacity)
	print("EAN: " + str(ean))
	print("Link: " + product_link)
	print("Price: " + price)
	print("Currency: " + currency)
	print("Localização: " + origem)
