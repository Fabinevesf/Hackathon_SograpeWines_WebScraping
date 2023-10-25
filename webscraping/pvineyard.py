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
		raise ValueError("Could not find product")
	response = requests.get(product_link, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'})
	soup = BeautifulSoup(response.content, 'html.parser')

	file1 = open("myfile.txt","w")
	file1.write(str(soup))

	total = soup.find_all('span', class_='ttvpopup-carrent-price')[0].text
	total = total.replace('\n', '')
	result = re.findall(r'[0-9,]+', total)
	price = ''.join(result)
	
	try:
		element = soup.find_all('div', class_='product-discount')[0]
		discount = 1
	except:
		discount = 0

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
			if 'NV' in year:
				year = '0'
			break
		else:
			year = None
	cur_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1)))

	print(ean)
	print(price)
	print(discount)
	print(cur_time)
	print(capacity)
	print(year)

	return[ean, "Portugal Vineyards", year, float(price.replace(',', '.')), discount, '€', cur_time, "Portugal"]

get_pvineyard(5902539714364)