from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

store_urls = [
    "https://store.playstation.com/it-it/product/",
    "https://store.playstation.com/en-us/product/",
    "https://store.playstation.com/en-gb/product/",
    # Puoi reinserire tutte le altre regioni qui
]

def setup_driver(chromedriver_path):
    options = Options()
    options.add_argument("--headless")  # Nasconde il browser
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(executable_path=chromedriver_path, options=options)

def estrai_dati(driver, url):
    driver.get(url)
    time.sleep(4)  # Attesa caricamento contenuti dinamici

    try:
        titolo = driver.find_element(By.TAG_NAME, "h1").text.strip()
    except:
        titolo = "Titolo non trovato"

    try:
        prezzo = driver.find_element(By.XPATH, "//span[contains(text(),'€')]").text.strip()
    except:
        prezzo = "Prezzo non disponibile"

    try:
        descrizione = driver.find_element(By.CSS_SELECTOR, '[data-qa="gameDesc"]').text.strip()
    except:
        descrizione = "Descrizione non trovata"

    # Ricerca lingue
    lingue_voce = "Non disponibili"
    lingue_schermo = "Non disponibili"

    try:
        blocchi_info = driver.find_elements(By.CLASS_NAME, "psw-l-line-left")
        for b in blocchi_info:
            testo = b.text.lower()
            if "lingua parlata" in testo or "voice" in testo:
                lingue_voce = b.text.split(":")[-1].strip()
            elif "lingua dello schermo" in testo or "screen language" in testo:
                lingue_schermo = b.text.split(":")[-1].strip()
    except:
        pass

    return {
        "titolo": titolo,
        "prezzo": prezzo,
        "descrizione": descrizione,
        "lingue_voce": lingue_voce,
        "lingue_schermo": lingue_schermo
    }

# === MAIN ===
codice_prodotto = "EP0700-PPSA25381_00-ERSL000000000000"
chromedriver_path = r"C:\percorso\al\tuo\chromedriver.exe"  # ← MODIFICA QUESTO

driver = setup_driver(chromedriver_path)

for base_url in store_urls:
    regione = base_url.split("/")[3]
    url = base_url + codice_prodotto
    try:
        dati = estrai_dati(driver, url)
        print(f"🗺️ Regione: {regione}")
        print(f"  🎮 Titolo: {dati['titolo']}")
        print(f"  💰 Prezzo: {dati['prezzo']}")
        print(f"  📘 Descrizione: {dati['descrizione'][:150]}...")
        print(f"  📺 Lingue Schermo: {dati['lingue_schermo']}")
        print(f"  🗣️ Lingue Voce: {dati['lingue_voce']}")
        print(f"  🔗 URL: {url}\n")
    except Exception as e:
        print(f"⚠️ Errore per regione {regione}: {str(e)}\n")

driver.quit()
