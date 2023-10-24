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
	website = "Garrafeira Soares"

	soup = BeautifulSoup(response.content, "html.parser")
	link = soup.find_all('script')[0]
	url_match = re.search(r"location='(.*?)'", link.text)
	url = url_match.group(1)

	response = requests.get(url)

	soup = BeautifulSoup(response.content, "html.parser")
	price = soup.find_all('h2', class_='clearfix')[0].text
	name = soup.find_all('div', class_='name clearfix')[0].text
	name = name.strip()
	price,currency = find_and_save_character(price, '€')
	price = price.strip()
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
	
	print("Name: " + name)
	print("Ano: None")
	print("Capacidade: " + capacity)
	print("Current price is" + currency + price)
	now = datetime.datetime.now()
	return [now, website, name, price+currency, capacity]