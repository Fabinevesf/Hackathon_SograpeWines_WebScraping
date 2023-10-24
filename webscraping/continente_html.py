from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_continente_html(ean):
	# Set options
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')

	# Set up the webdriver
	driver = webdriver.Chrome(options=options)

	# Navigate to the webpage
	driver.get("https://www.continente.pt/")

	driver.maximize_window()

	wait = WebDriverWait(driver, 10)
	try:
		button = wait.until(EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")))
		button.click()
	except:
		pass

	button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="brand-header"]/div[2]/div/div/ul[2]/li[4]/button')))
	button.click()

	input_field = wait.until(EC.element_to_be_clickable((By.ID, 'coverage-postal-code')))
	input_field.click()
	input_field.send_keys('Porto')

	button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="coverage-area-modal"]/div/div/div[2]/div/div[2]/div[2]/form/div/div[2]/div[1]/button[2]')))
	button.click()

	button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="store-col-1905-store"]/div[1]/label')))
	button.click()

	button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm-coverage-area-modal"]/div/div/div[2]/div/div[2]/button[2]')))
	button.click()

	time.sleep(5)

	url = "https://www.continente.pt/pesquisa/?q=" + ean
	driver.get(url)

	soup = BeautifulSoup(driver.page_source, "html.parser")

	products = soup.find_all('div', class_='product')
	if len(products) == 0:
		driver.quit()
		print("No products found")
		return None
	product = products[0]
	url = product.find_all('a')[0]['href']
	driver.get(url)

	return driver.page_source