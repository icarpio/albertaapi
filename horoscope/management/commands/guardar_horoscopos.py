from django.core.management.base import BaseCommand
from horoscope.models import Horoscopo
from datetime import date
import requests
from bs4 import BeautifulSoup

SIGNOS = [
    "ARIES", "TAURO", "GÉMINIS", "CÁNCER",
    "LEO", "VIRGO", "LIBRA", "ESCORPIO",
    "SAGITARIO", "CAPRICORNIO", "ACUARIO", "PISCIS"
]

BASE_URL = "https://www.hola.com/horoscopo/"

def obtener_url_horoscopo_hoy():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/horoscopo/" in href and "horoscopo-de-hoy" in href:
            return "https://www.hola.com" + href if href.startswith("/") else href
    return None

def extraer_horoscopos(url):
    response = requests.get(url)
    if response.status_code != 200:
        return {}
    soup = BeautifulSoup(response.content, "html.parser")
    horoscopos = {}
    for signo in SIGNOS:
        encabezado = soup.find(lambda tag: tag.name in ["h2","h3","h4"] and signo in tag.get_text().upper())
        if not encabezado:
            continue
        texto = ""
        for sib in encabezado.next_siblings:
            if getattr(sib, "name", None) == "p":
                texto = sib.get_text().strip()
                break
        horoscopos[signo] = texto
    return horoscopos

class Command(BaseCommand):
    help = 'Guarda horóscopos diarios en la base de datos'

    def handle(self, *args, **kwargs):
        url_hoy = obtener_url_horoscopo_hoy()
        if not url_hoy:
            self.stdout.write("No se pudo obtener la URL del horóscopo de hoy.")
            return
        horoscopos = extraer_horoscopos(url_hoy)
        for signo, texto in horoscopos.items():
            Horoscopo.objects.update_or_create(
                signo=signo,
                fecha=date.today(),
                defaults={"texto": texto}
            )
        self.stdout.write(self.style.SUCCESS("Horóscopos guardados correctamente."))
