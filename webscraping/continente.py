import requests
from bs4 import BeautifulSoup

def get_continente(ean):
	url = "https://www.continente.pt/pesquisa/?q="
	url = url + ean
	response = requests.get(url, cookies={'dwsid':'LT_YtM8_xZLDvEwyRBXjSC6dy1q8yJAAIp0NZvBa_9lRBvwesJi5jtM6UMA741GwX70rTTcG3nFyUSyBS6pH3Q=='}, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})

	soup = BeautifulSoup(response.content, "html.parser")

	try:
		product = soup.find_all('div', class_='ct-image-container')[0]
	except:
		print("Product Not found")
		return NULL
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
	time = time.asctime(time.localtime())
	
	try:
		discount = (soup.find_all('span', class_='ct-product-tile-badge-value--pvpr col-product-tile-badge-value--pvpr'))[0].text
		discount = 1
	except:
		discount = 0

	print(discount)

	return[ean, "Continente", price, discount, currency, time, origem]