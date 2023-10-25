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
	
	data_list = soup.find_all('dl', class_='data-sheet')[0]
	data_names = data_list.find_all('dt', class_='name')
	data_values = data_list.find_all('dd', class_='value')

	for i in range(len(data_names)):
		if data_names[i].text == "Capacidade":
			capacity = data_values[i].text
			break
		else:
			capacity = None
		if data_names[i].text == "Colheita":
			year = data_values[i].text
			break
		else:
			year = None
	cur_time = datetime.datetime.now()
	print(ean)
	print(price)
	print(discount)
	print(currency)
	print(cur_time)

get_pvineyard(5601012004427)