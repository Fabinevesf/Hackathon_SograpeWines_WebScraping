import requests
from bs4 import BeautifulSoup

def get_continente(ean):
	url = "https://www.continente.pt/pesquisa/?q=5601012001310"
	response = requests.get(url)

	soup = BeautifulSoup(response.content, "html.parser")

	product = soup.find_all('div', class_='ct-image-container')[0]

	product_link = product.find_all('a')[0]['href']

	website = "Continente"

	response = requests.get(product_link)

	soup = BeautifulSoup(response.content, "html.parser")

	price = soup.find_all('span', class_='ct-price-formatted')[0].text

	name = soup.find_all('h1', class_='product-name')[0].text

	capacity = (soup.find_all('span', class_='ct-pdp--unit col-pdp--unit'))[0].text
	capacity = capacity.replace("garrafa ", "")


	print("From website" + website)
	print("Bottle name" + name)
	print("Current price is" + price)
	print("Bottle capacity is" + capacity)