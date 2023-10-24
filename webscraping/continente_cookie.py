from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

def get_continente_cookie(ean):
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

	button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="product-search-results"]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/a/picture/img')))
	button.click()

	time.sleep(5)

	return driver.page_source