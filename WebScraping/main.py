import requests
from bs4 import BeautifulSoup
import pandas as pd
from scraper_functions import scrape_dom_details


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

        links_container = soup.find('select', id="zupanije")
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
            # TODO: Fix logic here 
            dom_linkovi = soup_zupanija.find_all('div', class_='listing domovi my-4')
            
           
            dom_url_ovi = []
            for dom_article in dom_linkovi:
                link_elements = dom_article.find_all('h2', class_='entry-title dom-title')
                for link_element in link_elements:
                    a_tag = link_element.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        dom_url_ovi.append(a_tag['href'])

            print(f"Found {len(dom_url_ovi)} for processing.")

          
            for url_nursing in dom_url_ovi:
                print(f" > Getting nursing details from: {url_nursing}")

                dom_podaci = scrape_dom_details(url_nursing)

                if dom_podaci:
                    svi_domovi_podatci.append(dom_podaci) # TO HERE FIX 
                # ------------------------------------------------------------
        except requests.exceptions.RequestException as e:
            print(f"Error fetching county page {url_zupanija}: {e}")
            continue
    

    if svi_domovi_podatci:
        df = pd.DataFrame(svi_domovi_podatci).where(pd.notnull, 'Null')


        try:
            df.to_excel('nursing_homes_data.xlsx', index=False, engine='openpyxl')
            print("Data successfully saved to nursing_homes_data.xlsx")
        except Exception as e:
            print(f"Error saving data to Excel: {e}")
    else:
        print("No nursing home data collected.")
        


if __name__ == "__main__":
    scrape_domovi()