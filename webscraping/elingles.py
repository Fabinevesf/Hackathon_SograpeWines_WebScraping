import requests
from bs4 import BeautifulSoup

def get_elingles(ean):
	url = "https://www.elcorteingles.pt/supermercado/pesquisar/?term=" + str(ean)

	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	print(soup)
	product_link = soup.find_all('a', class_='product-link')[0]['href']
	print(product_link)