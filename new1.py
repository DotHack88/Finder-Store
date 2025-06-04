import requests

def cerca_gioco_api(gioco, paese='IT', lingua='it'):
    query = gioco.replace(" ", "+")
    url = f"https://store.playstation.com/store/api/chihiro/00_09_000/search/{paese}/{lingua}?query={query}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return {"errore": f"Errore {res.status_code} nella richiesta API"}

    data = res.json()
    risultati = data.get("links", [])
    if not risultati:
        return {"errore": "Nessun risultato trovato"}

    # Prende il primo risultato
    gioco_info = risultati[0]

    return {
        "titolo": gioco_info.get("name"),
        "descrizione": gioco_info.get("long_desc"),
        "prezzo_locale": gioco_info.get("default_sku", {}).get("price", {}).get("display_price"),
        "valuta": gioco_info.get("default_sku", {}).get("price", {}).get("currency"),
        "link": "https://store.playstation.com" + gioco_info.get("url", "")
    }

# Test
if __name__ == "__main__":
    risultato = cerca_gioco_api("astro bot", paese="IT", lingua="it")
    print(risultato)
