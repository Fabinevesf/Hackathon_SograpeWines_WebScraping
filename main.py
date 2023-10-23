from webscraping.continente import get_continente
from webscraping.garrafeirasoares import get_garrafeira_soares
from webscraping.elingles import get_elingles

ean = input('EAN: ')

get_continente(ean)
get_garrafeira_soares(ean)
get_elingles(ean)