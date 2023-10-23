from webscraping.continente import get_continente
from webscraping.garrafeirasoares import get_garrafeira_soares
ean = input('EAN: ')

print(ean)
get_continente(ean)
get_garrafeira_soares(ean)