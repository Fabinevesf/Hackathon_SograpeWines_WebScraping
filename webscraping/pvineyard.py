from bs4 import BeautifulSoup
import datetime
import requests

#NOME ANO CAPACIDADE EAN WEBSITE LINK PREÇO MOEDA LOCALIZAÇÃO

def get_pvineyard(ean):
	url = 'https://www.portugalvineyards.com/pt/search?s=' + str(ean)

	
	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	product_link = soup.find_all('a', class_='thumbnail product-thubmnail')[0]['href'].text
	response = requests.get(product_link, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')
