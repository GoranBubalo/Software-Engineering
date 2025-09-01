import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


# TODO: Refactor croatian to english

def get_zupanije_urls():
    pocetna_url = 'https://www.domovi-za-starije.com/'

    # Mimic a web browser - Special ClientID 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'hr,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    try:
        response = requests.get(pocetna_url, headers=headers)

        print(f"Statusni kod zahtjeva: {response.status_code}")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup.prettify())  # What are we getting back?

        links_container = soup.find('select', id="zupanije") # Error 

        if links_container:
            zupanije = {}
            for opcija in links_container.find_all('option'):
                naziv_zupanije = opcija.text.strip()
                url_zupanije = opcija.get('value')
                
                if url_zupanije and url_zupanije != '':
                    zupanije[naziv_zupanije] = url_zupanije
            return zupanije
        else:
            print("Nije pronaden popis zupanija na stranici")
            return []
        
    except requests.exceptions.RequestException as e:
        print(f"Dogodila se greska prilikom dohvacanja stranice: {e}")
        return []    


def scrape_domovi():
    zupanije_urls = get_zupanije_urls()

    if not zupanije_urls:
        print("Scraping nije moguc jer nema dostupnih URL-ova zupanija.")
        return 
    
    print(f"Automatski prikupljeno {len(zupanije_urls)} URL-ova zupanija.")

    ## Iterating through each county URL to get nursing home links
    svi_domovi_podatci = []
    for naziv_zupanija, url_zupanija in zupanije_urls.items():
        print (f"--Scraping zupanije: {len(naziv_zupanija)} -----")

        try:
            response_zupanija = requests.get(url_zupanija)
            response_zupanija.raise_for_status()
            soup_zupanija = BeautifulSoup(response_zupanija.text, 'html.parser')

            dom_linkovi = soup_zupanija.find_all('article', class_='dom hentry')
            
            # TODO: Extract nursing home URLs from the articles

            print(f"Found {len(dom_url_ovi)} for processing.")

            # Scraping and visiting each nursing home link
            for url_nursing in dom_url_ovi:
                print(f" > Getting nursing details from: {url_nursing}")

                # TODO: logic for getting and processing nursing home details
                
                # Excample of adding to the list
                nursing_data = {'Name': 'Example nursing', 'Address': 'Example address', 'Telephone': '123456789', 'County_URL': url_zupanija}
                svi_domovi_podatci.append(nursing_data)
                time.sleep(1.5)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching county page {url_zupanija}: {e}")
            continue
    
    # Storing in excel
    if svi_domovi_podatci:
        df = pd.DataFrame(svi_domovi_podatci)

        # Storing data in excel
        try:
            df.to_excel('nursing_homes_data.xlsx', index=False, engine='openpyxl')
            print("Data successfully saved to nursing_homes_data.xlsx")
        except Exception as e:
            print(f"Error saving data to Excel: {e}")
    else:
        print("No nursing home data collected.")
        


if __name__ == "__main__":
    scrape_domovi()