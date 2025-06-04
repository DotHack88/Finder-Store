import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore, Style, init

init(autoreset=True)

STORE_URLS = [
    "https://store.playstation.com/it-it/product/",
    "https://store.playstation.com/tr-tr/product/",
    "https://store.playstation.com/en-in/product/",
    "https://store.playstation.com/ru-ru/product/",
    "https://store.playstation.com/en-za/product/",
    "https://store.playstation.com/en-se/product/",
    "https://store.playstation.com/da-dk/product/",
    "https://store.playstation.com/en-ae/product/",
    "https://store.playstation.com/en-gb/product/",
    "https://store.playstation.com/en-no/product/",
    "https://store.playstation.com/de-ch/product/",
    "https://store.playstation.com/en-au/product/",
    "https://store.playstation.com/en-ca/product/",
    "https://store.playstation.com/en-il/product/",
    "https://store.playstation.com/es-mx/product/",
    "https://store.playstation.com/en-nz/product/",
    "https://store.playstation.com/en-hk/product/",
    "https://store.playstation.com/ja-jp/product/",
    "https://store.playstation.com/en-us/product/",
    "https://store.playstation.com/en-id/product/",
    "https://store.playstation.com/pt-br/product/",
    "https://store.playstation.com/es-ar/product/",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

known_languages = [
    "italiano", "english", "francese", "spanish", "portuguese", "deutsch", "nederlands", "svenska", "danish", "norwegian", "finnish", "russian", "polski", "čeština", "magyar", "română", "slovenčina", "български", "hrvatski", "srpski", "slovenski", "ukrainian", "العربية", "עברית", "हिन्दी", "ภาษาไทย", "tiếng việt", "bahasa indonesia", "filipino", "malay", "korean", "中文", "日本語", "русский", "български", "hrvatski", "srpski", "slovenski", "ukrainian", "العربية", "עברית", "हिन्दी", "ภาษาไทย", "tiếng việt", "bahasa indonesia", "filipino", "malay", "korean", "中文", "日本語"
]

lang_regex = re.compile(r'\b(' + '|'.join(known_languages) + r')\b', re.IGNORECASE)

def extract_languages(soup):
    # Cerca direttamente i tag con gli attributi data-qa specifici
    audio_tag = soup.find(attrs={"data-qa": "gameInfo#releaseInformation#voice-value"})
    screen_tag = soup.find(attrs={"data-qa": "gameInfo#releaseInformation#subtitles-value"})

    # Estrai e pulisci le lingue
    audio_langs = []
    screen_langs = []
    if audio_tag and audio_tag.text.strip():
        audio_langs = [l.strip() for l in audio_tag.text.split(",") if l.strip()]
    if screen_tag and screen_tag.text.strip():
        screen_langs = [l.strip() for l in screen_tag.text.split(",") if l.strip()]

    return audio_langs, screen_langs

def get_exchange_rate(currency_code):
    if currency_code.upper() == "EUR":
        return 1.0
    try:
        url = f"https://api.exchangerate.host/latest?base={currency_code.upper()}&symbols=EUR"
        res = requests.get(url, timeout=5)
        data = res.json()
        return data["rates"]["EUR"]
    except Exception:
        return None

def extract_price_and_currency(price_str):
    # Cerca simbolo e valuta
    price_str = price_str.replace('\xa0', ' ')
    patterns = [
        (r'€\s?([\d,.]+)', 'EUR'),
        (r'([\d,.]+)\s?€', 'EUR'),
        (r'£\s?([\d,.]+)', 'GBP'),
        (r'([\d,.]+)\s?£', 'GBP'),
        (r'(\d[\d,.]*)\s?TL', 'TRY'),
        (r'(\d[\d,.]*)\s?Kr', 'SEK'),
        (r'(\d[\d,.]*)\s?kr', 'NOK'),
        (r'CHF\s?([\d,.]+)', 'CHF'),
        (r'R\s?([\d,.]+)', 'ZAR'),
        (r'ILS\s?([\d,.]+)', 'ILS'),
        (r'Rs\s?([\d,.]+)', 'INR'),
        (r'Rp\s?([\d,.]+)', 'IDR'),
        (r'\$([\d,.]+)', 'USD'),
        (r'([\d,.]+)\s?\$', 'USD'),
        (r'([\d,.]+)\s?AUD', 'AUD'),
        (r'([\d,.]+)\s?CAD', 'CAD'),
        (r'([\d,.]+)\s?MXN', 'MXN'),
        (r'([\d,.]+)\s?BRL', 'BRL'),
        (r'([\d,.]+)\s?ARS', 'ARS'),
        # aggiungi altri pattern se necessario
    ]
    for pattern, code in patterns:
        match = re.search(pattern, price_str)
        if match:
            value = match.group(1).replace('.', '').replace(',', '.')
            try:
                return float(value), code
            except Exception:
                return None, None
    return None, None

def fetch_game_info(game_id):
    results = []
    for store_url in STORE_URLS:
        url = f"{store_url}{game_id}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            results.append({'store': store_url, 'title': 'N/A', 'price': 'N/A', 'price_eur': 'N/A', 'audio_languages': [], 'screen_languages': []})
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Titolo
        title = 'N/A'
        h1_tag = soup.find('h1', {'data-qa': 'mfe-game-title#name'})
        if h1_tag and h1_tag.text.strip():
            title = h1_tag.text.strip()
        else:
            span_tag = soup.find('span', class_="psw-m-b-5 psw-t-title-l psw-t-size-8 psw-l-line-break-word")
            if span_tag and span_tag.text.strip():
                title = span_tag.text.strip()
            else:
                title_tag = soup.find('title')
                if title_tag and title_tag.text.strip():
                    title = title_tag.text.replace("su PlayStation™Store", "").replace("| Acquista online", "").strip(" -|")

        # Prezzo
        price_tag = soup.find('span', {'data-qa': 'mfeCtaMain#offer0#finalPrice'})
        price = price_tag.text.strip() if price_tag else 'N/A'

        # Conversione in euro
        price_value, currency = extract_price_and_currency(price)
        price_eur = 'N/A'
        if price_value and currency:
            rate = get_exchange_rate(currency)
            if rate:
                price_eur = round(price_value * rate, 2)

        # Lingue audio e a schermo
        audio_langs, screen_langs = extract_languages(soup)

        results.append({
            'store': store_url,
            'title': title,
            'price': price,
            'price_eur': price_eur,
            'audio_languages': audio_langs,
            'screen_languages': screen_langs
        })
    return results

def mostra_ultimi_giochi():
    url = "https://store.playstation.com/it-it/category/e1699f77-77e1-43ca-a296-26d08abacb0f/"
    print(f"{Fore.CYAN}{'🟦'*20}")
    print(f"{Fore.YELLOW}Estrazione degli ultimi giochi dal PlayStation Store...{Style.RESET_ALL}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        giochi = []
        # Cerca i giochi nei tag <a> con href contenente "/product/"
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/product/' in href:
                titolo = a.text.strip()
                id_gioco = href.split('/product/')[-1]
                if titolo and id_gioco:
                    giochi.append((titolo, id_gioco))
            if len(giochi) >= 5:
                break
        if not giochi:
            print(f"{Fore.RED}Nessun gioco trovato!{Style.RESET_ALL}")
            return
        print(f"{Fore.YELLOW}Ecco alcuni degli ultimi giochi usciti su PlayStation Store:{Style.RESET_ALL}")
        for idx, (nome, id_gioco) in enumerate(giochi, 1):
            print(f"{Fore.WHITE}{idx}. {nome} {Fore.LIGHTBLACK_EX}- ID: {id_gioco}")
        scelta = input(f"{Fore.YELLOW}Se vuoi vedere i dettagli di un gioco, inserisci il numero (oppure premi invio per tornare al menu): {Fore.WHITE}").strip()
        if scelta.isdigit() and 1 <= int(scelta) <= len(giochi):
            nome, id_gioco = giochi[int(scelta)-1]
            infos = fetch_game_info(id_gioco)
            for info in infos:
                print(f"{Fore.CYAN}{'🟦'*20}")
                print(f"{Fore.YELLOW}🌍 Store: {Fore.WHITE}{info['store']}")
                print(f"{Fore.GREEN}🎮 Titolo: {Fore.WHITE}{info['title']}")
                print(f"{Fore.MAGENTA}💰 Prezzo: {Fore.WHITE}{info['price']} {Fore.LIGHTBLACK_EX}| 💶 Prezzo in EUR: {Fore.WHITE}{info['price_eur']}")
                print(f"{Fore.BLUE}🔊 Lingue audio: {Fore.WHITE}{', '.join(info['audio_languages']) if info['audio_languages'] else 'N/A'}")
                print(f"{Fore.BLUE}📝 Lingue a schermo: {Fore.WHITE}{', '.join(info['screen_languages']) if info['screen_languages'] else 'N/A'}")
            print(f"{Fore.CYAN}{'🟦'*20}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Torno al menu principale...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Errore durante lo scraping: {e}{Style.RESET_ALL}")

def popup_inserisci_id():
    import tkinter as tk
    from tkinter import simpledialog
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale
    id_gioco = simpledialog.askstring("Inserisci ID gioco", "Inserisci l'ID del gioco (es: EP0700-PPSA25381_00-ERSL000000000000):")
    root.destroy()
    return id_gioco

if __name__ == "__main__":
    print(f"{Fore.CYAN}{'🟦'*20}")
    print(f"{Fore.YELLOW}🎮 Benvenuto nel PlayStation Store Scraper!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'🟦'*20}")
    print(f"{Fore.LIGHTRED_EX}⚠️  Questo programma è opera di Emanuele Barese ed è vietato l'uso e la commercializzazione!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'🟦'*20}")

    print(f"{Fore.GREEN}Cosa vuoi cercare?")
    print(f"{Fore.WHITE}1. 🔎 Cerca per ID gioco (consigliato)")
    print(f"{Fore.WHITE}2. ❌ Esci")
    print(f"{Fore.WHITE}3. ℹ️ Info sul programma")
    scelta = input(f"{Fore.YELLOW}Seleziona un'opzione (1-3): {Fore.WHITE}").strip()

    if scelta == "1":
        game_id = input(f"{Fore.YELLOW}Inserisci l'ID del gioco (es: EP0700-PPSA25381_00-ERSL000000000000): {Fore.WHITE}").strip()
        if not game_id:
            print(f"{Fore.RED}Nessun ID inserito. Torno al menu.{Style.RESET_ALL}")
        else:
            infos = fetch_game_info(game_id)
            for info in infos:
                print(f"{Fore.CYAN}{'🟦'*20}")
                print(f"{Fore.YELLOW}🌍 Store: {Fore.WHITE}{info['store']}")
                print(f"{Fore.GREEN}🎮 Titolo: {Fore.WHITE}{info['title']}")
                print(f"{Fore.MAGENTA}💰 Prezzo: {Fore.WHITE}{info['price']} {Fore.LIGHTBLACK_EX}| 💶 Prezzo in EUR: {Fore.WHITE}{info['price_eur']}")
                print(f"{Fore.BLUE}🔊 Lingue audio: {Fore.WHITE}{', '.join(info['audio_languages']) if info['audio_languages'] else 'N/A'}")
                print(f"{Fore.BLUE}📝 Lingue a schermo: {Fore.WHITE}{', '.join(info['screen_languages']) if info['screen_languages'] else 'N/A'}")
            print(f"{Fore.CYAN}{'🟦'*20}{Style.RESET_ALL}")
    elif scelta == "2":
        print(f"{Fore.RED}Uscita dal programma. Arrivederci!{Style.RESET_ALL}")
    elif scelta == "3":
        print(f"{Fore.CYAN}ℹ️  Questo programma ti permette di confrontare prezzi e lingue dei giochi PlayStation Store nei vari paesi!{Style.RESET_ALL}")
        print(f"{Fore.LIGHTRED_EX}⚠️  Opera di Emanuele Barese. Vietato l'uso e la commercializzazione!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🔜 Prossimamente: ricerca per nome, filtri avanzati e molto altro!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Opzione non valida. Uscita dal programma.{Style.RESET_ALL}")