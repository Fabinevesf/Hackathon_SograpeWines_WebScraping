from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
import re

def get_granvine(ean):
	url = 'https://granvine.com/pt/catalogsearch/result/?q=' + str(ean)

	# Set options
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')

	# Set up the webdriver
	driver = webdriver.Chrome(options=options)

	# Navigate to the webpage
	driver.get(url)
	driver.maximize_window()

	wait = WebDriverWait(driver, 20)
	wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.Button[value="yes"]'))).click()
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	product_list = soup.find_all('div', class_='search results')[0]
	products = product_list.find_all('li', class_='product-item')
	if products == (None or []):
		driver.quit()
		raise Exception('Granvine: Product not found.')
	wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-bind="attr: {href: url}"]'))).click()
	wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.product-custom-info-title')))

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	driver.quit()

	price = soup.find_all('span', class_='price')[0].text.replace('\xa0', ' ')
	currency = price.split(' ')[1]
	price = price.replace(',', '.')
	price = price.split(' ')[0]


	capacity = soup.find_all('div', class_='capacity')[0]
	capacity = capacity.find_all('span')[0].text
	capacity = re.findall(r'\d+', capacity)[0]

	location = soup.find_all('div', class_='country')[0]
	location = location.find_all('span')[0].text

	discount = soup.find_all('div', class_='product-main-info')[0]
	try:
		discount = discount.find_all('span', class_='special-price-discount')[0]
		discount = 1
	except:
		discount = 0

	characteristics = soup.find_all('div', class_='characteristics')[0]
	title = characteristics.find_all('span')
	description = characteristics.find_all('strong')
	year = 0

	for i in range(len(title)):
		if 'Ano da colheita: ' in title[i].text:
			year = description[i].text

	img = soup.find_all('img', id='magnifier-item-0')[0]['src']

	#print(ean)
	#print(year)
	#print(price)
	#print(discount)
	#print(currency)
	#print(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1))))
	#print(location)

	return [ean, "Granvine", year, float(price), discount, currency, datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=1))), location, url]