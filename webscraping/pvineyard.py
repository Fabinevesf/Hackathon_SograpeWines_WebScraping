from bs4 import BeautifulSoup
import datetime
import requests

#NOME ANO CAPACIDADE EAN WEBSITE LINK PREÇO MOEDA LOCALIZAÇÃO

def get_pvineyard(ean):
	url = 'https://www.portugalvineyards.com/pt/search?s=' + str(ean)

	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	file1 = open("myfile.txt","w")
	file1.write(str(soup))

	product_link = soup.find_all('a', class_='thumbnail product-thumbnail')[0]['href']
	response = requests.get(product_link, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	file1 = open("myfile.txt","w")
	file1.write(str(soup))

	total = soup.find_all('span', class_='ttvpopup-carrent-price')[0].text
	total = total.replace('\n', '')
	currency = total[0]
	price = total[1::1]
	discount = 0

	name = soup.find_all('p', class_='product_name')[0].text
	name = name.replace("\n", "")
	name = name.split(" ")
	if name[len(name) - 1].isdigit():
		year = name[len(name) - 1]
	else:
		year = "N/A"
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
	try:
		origem = (soup.find_all('p', class_='mb-20'))[2].text
		origem = origem.replace('\n', '')
	except:
		origem = "N/A"
	cur_time = datetime.datetime.now()
	try:
		discount = (soup.find_all('div', class_='ct-product-tile-badge-value-wrapper col-product-tile-badge-value-wrapper ct-product-tile-badge-value-wrapper--pvpr col-product-tile-badge-value-wrapper--pvpr   '))[0].text
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
get_pvineyard(5601012004427)