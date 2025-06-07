import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://store.playstation.com/it-it/category/488b6df1-3b55-45b0-b7c7-4e3b35c56d57"
headers = {
    "User-Agent": "Mozilla/5.0"
}

games = []

for page in range(1, 123):  # 122 pagine
    url = f"{base_url}/{page}"
    print(f"Scarico pagina {page}...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Errore nella pagina {page}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # ATTENZIONE: selettori CSS dipendono dal sito attuale (potrebbero cambiare!)
    cards = soup.select('[data-qa="product-card-name"]')

    if not cards:
        print(f"Nessun gioco trovato in pagina {page}.")
        continue

    for card in cards:
        title = card.get_text(strip=True)
        parent = card.find_parent("a")
        link = "https://store.playstation.com" + parent["href"] if parent else "N/A"

        price_elem = parent.select_one('[data-qa="strike-price"]')
        discounted_elem = parent.select_one('[data-qa="display-price"]')

        original_price = price_elem.get_text(strip=True) if price_elem else ""
        discounted_price = discounted_elem.get_text(strip=True) if discounted_elem else ""

        games.append({
            "Nome": title,
            "Prezzo": discounted_price,
            "Prezzo Originale": original_price,
            "Link": link
        })

    time.sleep(0.5)

# Esporta tutto
df = pd.DataFrame(games)
df.to_csv("giochi_scraping_html.csv", index=False)
print("✅ File completato: giochi_scraping_html.csv")
