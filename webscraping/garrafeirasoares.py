import requests
import re
from bs4 import BeautifulSoup

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
  price = price.replace('\t', '')
  price,currency = find_and_save_character(price, '€')
  price = price.replace(' ', '')
  price = price.replace('\n', '')

  capacity = soup.find_all('div', class_='col-sm-8 column column-info')[4].text
  capacity

  print("From website - " + website + "\n")
  print("Bottle name" + name)
  print("Current price is\n" + currency + price)
  print("Bottle capacity is" + capacity)