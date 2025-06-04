from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def get_exchange_rate_xe(from_currency, to_currency='EUR'):
    url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From={from_currency}&To={to_currency}"

    # Setup driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Nasconde il browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    time.sleep(3)  # Attendi caricamento pagina (a volte serve di più)

    try:
        # Cerca il div con il tasso di cambio
        rate_element = driver.find_element(By.CLASS_NAME, 'result__BigRate-sc-1bsijpp-1')
        rate_text = rate_element.text.strip().split(' ')[0].replace(',', '')
        rate = float(rate_text)
        return rate
    except Exception as e:
        print(f"Errore durante il parsing: {e}")
        return None
    finally:
        driver.quit()

# Esempio:
print(f"1 TRY = {get_exchange_rate_xe('TRY')} EUR")
print(f"1 USD = {get_exchange_rate_xe('USD')} EUR")
