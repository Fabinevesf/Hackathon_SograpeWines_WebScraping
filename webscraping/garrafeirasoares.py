import requests
import re
from bs4 import BeautifulSoup
import datetime

def find_and_save_character(string, character):
  match = re.search(r'{}'.format(character), string)
  if match:
    saved_character = match.group()
    new_string = string.replace(saved_character, '')
    return new_string, saved_character
  else:
    return string, None

def get_garrafeira_soares(ean):
	url = "https://www.garrafeirasoares.pt/pt/resultado-da-pesquisa_36.html?term=" + str(ean)
	response = requests.get(url)
	StoreName = "Garrafeira Soares"

	soup = BeautifulSoup(response.content, "html.parser")
	no_results = soup.find('h1', string='Pesquisa sem resultados ')
	if no_results:
		raise Exception('Garrafeira Soares: Product not found.')
	link = soup.find_all('script')[0]
	url_match = re.search(r"location='(.*?)'", link.text)
	url = url_match.group(1)

	response = requests.get(url)

	discount = 0
	soup = BeautifulSoup(response.content, "html.parser")
	price = soup.find_all('h2', class_='clearfix')[0].text
	name = soup.find_all('div', class_='name clearfix')[0].text
	name = name.strip()
	price,currency = find_and_save_character(price, '€')
	price = price.strip()
	price = price.replace(',','.')
	currency = currency.strip()

	capacity = soup.find_all('div', class_='col-sm-4 column column-head')
	for i in capacity:
		if ("Capacidade" in i.text):
			capacity = i.find_next_sibling()
			capacity = capacity.text
			capacity = capacity.replace('\n','')
			capacity = float(capacity.split(' ')[0])
			capacity *= 1000
			capacity = int(capacity)
			break

	try:
		discount = (soup.find_all('span', class_='discount'))[0].text
		discount = 1
	except:
		discount = 0

	# print("Name: " + name)
	# print("Ano: None")
	# print("Capacidade: ", capacity)
	# print("Current price is" + currency + price)
	# print(discount)
	now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1)))
	return [ean, StoreName, "0", str(price), str(discount), currency, str(now), 'Portugal', url]
