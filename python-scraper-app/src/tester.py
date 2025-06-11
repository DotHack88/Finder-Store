import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
}

def search_store_it(query, max_results=5):
    """Cerca giochi sullo store italiano"""
    print(f"Cerco '{query}' nello store italiano...")
    base_url = "https://store.playstation.com/it-it/search/"
    search_url = f"{base_url}{query.replace(' ', '%20')}"

    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('a', {'class': 'psw-link psw-content-link'})

        results = []
        for i, product in enumerate(products[:max_results]):
            href = product.get('href', '')
            title_element = product.find('span', {'data-qa': re.compile(r'product-name')})
            title = title_element.get_text(strip=True) if title_element else "N/A"
            price_element = product.find('span', {'data-qa': re.compile(r'display-price')})
            price = price_element.get_text(strip=True) if price_element else "N/A"

            results.append({
                'index': i + 1,
                'title': title,
                'price': price,
                'link': "https://store.playstation.com" + href
            })

        return results

    except Exception as e:
        print(f"Errore durante la ricerca: {e}")
        return []

def main():
    query = input("Inserisci il nome del gioco: ")
    results = search_store_it(query)

    if not results:
        print("Nessun risultato trovato.")
        return

    print("\nRisultati:")
    for r in results:
        print(f"{r['index']}. {r['title']} - {r['price']}")

    choice = input("\nScegli un numero per vedere i dettagli e altre offerte (q per uscire): ")
    if choice.lower() == 'q':
        return

    try:
        index = int(choice) - 1
        selected = results[index]
        print(f"\nHai selezionato: {selected['title']}")
        print(f"Link: {selected['link']}")

        sort = input("\nVuoi ordinare i risultati per prezzo? (min/max/nessuno): ").strip().lower()

        # Integrazione futura: cerca versioni regionali o multipiattaforma, poi filtra
        if sort == 'min':
            print("⚠️ Ordinamento per prezzo minimo non ancora implementato.")
        elif sort == 'max':
            print("⚠️ Ordinamento per prezzo massimo non ancora implementato.")

        lingua = input("Vuoi filtrare per lingua italiana? (s/n): ").strip().lower()
        if lingua == 's':
            print("⚠️ Filtro per lingua italiana non ancora implementato.")

    except (ValueError, IndexError):
        print("Scelta non valida.")

if __name__ == "__main__":
    main()
