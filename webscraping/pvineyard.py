from bs4 import BeautifulSoup
import datetime
import requests
import re

def get_pvineyard(ean):
	url = 'https://www.portugalvineyards.com/pt/search?s=' + str(ean)

	response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	product_table = soup.find_all('section', id='products')[0]
	try:
		product_link = product_table.find_all('a', class_='thumbnail product-thumbnail')[0]['href']
	except:
		raise Exception("Portugal Vineyards: Product not found")
	
	response = requests.get(product_link + "?SubmitCurrency=1&id_currency=1", headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	try:
		meta_tag = soup.find('meta', {'property': 'product:pretax_price:amount'})
		content = meta_tag['content']
		price = float(content)
		price += price * 0.13
		price = round(price, 2)
	except:
		raise Exception("Portugal Vineyards : Price not found")

	try:
		element = soup.find_all('div', class_='product-discount')[0]
		discount = 1
	except:
		discount = 0

	data_list = soup.find_all('dl', class_='data-sheet')[0]
	data_names = data_list.find_all('dt', class_='name')
	data_values = data_list.find_all('dd', class_='value')

	year = '0'
	for i in range(len(data_names)):
		if data_names[i].text == "Colheita":
			year = data_values[i].text
			if 'NV' in year:
				year = '0'
	cur_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1)))

	#print(ean)
	#print(price)
	#print(discount)
	#print(cur_time)
	#print(capacity)
	#print(year)

	return[ean, "Portugal Vineyards", year, price, discount, '€', cur_time, "Portugal", product_link]