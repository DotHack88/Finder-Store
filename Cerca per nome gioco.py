import requests
from bs4 import BeautifulSoup
import re

def search_playstation_store(query):
    """Search the PlayStation Store and return relevant products"""
    try:
        base_url = "https://store.playstation.com/it-it/search/"
        search_url = f"{base_url}{query.replace(' ', '%20')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    
    except Exception as e:
        print(f"Error accessing PlayStation Store: {e}")
        return None

def filter_products(soup, max_results=5):
    """Extract detailed product information from search results"""
    if not soup:
        return []
    
    products = soup.find_all('a', {'class': 'psw-link psw-content-link'})
    
    relevant_products = []
    
    for i, product in enumerate(products):
        if i >= max_results:
            break
            
        # Extract product ID from data-telemetry-meta
        telemetry_meta = product.get('data-telemetry-meta', '{}')
        product_id = re.search(r'"id":"([^"]+)"', telemetry_meta)
        product_id = product_id.group(1) if product_id else "N/A"
        
        # Extract title
        title_element = product.find('span', {'data-qa': re.compile(r'product-name')})
        title = title_element.get_text(strip=True) if title_element else "N/A"
        
        # Extract current price
        price_element = product.find('span', {'data-qa': re.compile(r'display-price')})
        price = price_element.get_text(strip=True) if price_element else "N/A"
        
        # Extract original price (strikethrough)
        original_price_element = product.find('s', {'data-qa': re.compile(r'price-strikethrough')})
        original_price = original_price_element.get_text(strip=True) if original_price_element else "N/A"
        
        # Extract discount percentage
        discount_element = product.find('span', {'data-qa': re.compile(r'discount-badge#text')})
        discount = discount_element.get_text(strip=True) if discount_element else "N/A"
        
        # Extract platform
        platform_element = product.find('span', {'data-qa': re.compile(r'game-art#tag0')})
        platform = platform_element.get_text(strip=True) if platform_element else "N/A"
        
        # Extract image URL
        img_element = product.find('img', {'data-qa': re.compile(r'game-art#image#image')})
        image_url = img_element.get('src') if img_element else "N/A"
        
        # Extract product link
        link = "https://store.playstation.com" + product['href'] if product.has_attr('href') else "#"
        
        relevant_products.append({
            'product_id': product_id,
            'title': title,
            'current_price': price,
            'original_price': original_price,
            'discount': discount,
            'platform': platform,
            'image_url': image_url,
            'link': link
        })
    
    return relevant_products

def display_results(products, query):
    """Display the search results in a detailed format"""
    if not products:
        print(f"\nNo products found for '{query}'.")
        print("\nSuggestions:")
        print("- Try different search terms")
        print("- Check your spelling")
        print("- Visit the official PlayStation Store website directly")
        return
    
    print(f"\nShowing first {len(products)} results for '{query}':")
    print("=" * 100)
    for i, product in enumerate(products, 1):
        print(f"\n{i}. {product['title']}")
        print(f"   Product ID: {product['product_id']}")
        print(f"   Platform: {product['platform']}")
        print(f"   Current Price: {product['current_price']}")
        if product['original_price'] != "N/A":
            print(f"   Original Price: {product['original_price']}")
        if product['discount'] != "N/A":
            print(f"   Discount: {product['discount']}")
        print(f"   Image URL: {product['image_url']}")
        print(f"   Store Link: {product['link']}")
        print("-" * 100)

def main():
    print("PlayStation Store Detailed Game Search")
    print("=" * 50)
    print("Note: Showing only first 5 results per search\n")
    
    while True:
        query = input("\nEnter game name to search (or 'quit' to exit): ").strip()
        if query.lower() == 'quit':
            break
            
        if not query:
            print("Please enter a search term.")
            continue
            
        print(f"\nSearching for '{query}'...")
        soup = search_playstation_store(query)
        products = filter_products(soup, max_results=5)
        display_results(products, query)

if __name__ == "__main__":
    main()
