import requests
from bs4 import BeautifulSoup

def get_elingles(ean):
	url = "https://www.elcorteingles.pt/supermercado/?term=" + str(ean)