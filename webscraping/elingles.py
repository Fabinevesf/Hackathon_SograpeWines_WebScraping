import requests
from bs4 import BeautifulSoup

#NOME ANO CAPACIDADE EAN WEBSITE LINK PREÇO MOEDA LOCALIZAÇÃO

def get_elingles(ean):
	url = "https://www.elcorteingles.pt/supermercado/pesquisar/?term=" + str(ean)

	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	product_link = soup.find_all('a', class_='js-product-link')[0]['href']
	product_link = "https://www.elcorteingles.pt" + product_link
	
	response = requests.get(product_link, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	name = soup.find_all('div', class_='pdp-title mb')[0].text.replace('\n', ' ')
	name = name.split(" garrafa")[0]
	if (name.endswith(" ")):
		name = name[:-1]

	capacity = soup.find_all('span', class_='info-key')
	for i in capacity:
		if (i.text == "Quantidade líquida:"):
			capacity = i.next_sibling.text.strip(' ')
			if "cl" in capacity:
				capacity = capacity.split(" ")[0] + "0 ml"
			if "Mililitros" in capacity:
				capacity = capacity.split(" ")[0] + " ml"
			break

	website = "elcorteingles"
	price = soup.find_all('div', class_='prices-price _current')[0].text
	currency = price.split(" ")[1]
	price = price.split(" ")[0]

	print("Name: " + name)
	print("Ano: " + str(None))
	print("Capacidade: " + capacity)
	print("EAN: " + str(ean))
	print("Website: " + website)
	print("Link: " + product_link)
	print("Price: " + price)
	print("Currency: " + currency)
	print("Localização: " + str(None))
	return name, None, capacity, ean, website, product_link, price, currency, None