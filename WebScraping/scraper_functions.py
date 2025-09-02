import requests
from bs4 import BeautifulSoup

# Getting details -> finding richest DOM   
def scrape_dom_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        detalji_doma = {
            'URL': url,
            'Naziv': '',
            'Adresa': '',
            'Telefoni': '',
            'Email': '',
            'Web_stranica': '',
            'Osnivac': '',
            'Predstavnica doma': '',
            'Pocetak rada': '',
            'Broj lezaja': '',
            'Jednokratne sobe': '',
            'Dvokratne sobe': '',
            'Trokatne sobe': '',
            'Stacionar/jedinica pojacane njege': '',
            'Apartmani': '',
            'Trajni': '',
            'Privremeni': '',
            'Dnevni boravak u domu': '',
            'Skrb o pokretnim osobama': '',
            'Skrb o nepokretnim osobama': '',
            'Skrb o psihickim bolesnim osobama': '',
            'Skrb o osobama s demencijom/Alyheimerom': '',
            'Palijativna skrb': '',
            'Zajednicke prostorije': '',
            'Dvoriste/vrt': '',
            'Lift': '',
            'Knjiznica': '',
            'Fizioterapeut': '',
            'Frizer/pediker': '',
            'Balkon/terasa': '',
            'SOS - sustav': '',
            'TV': '',
            'Klima': '',
            'WC': '',
            'Kupaona': '',
            'Mogućnost vlastitog namještaja': ''
        }

        # Name 
        naziv_element = soup.find('h1', class_='entry-title dom-title')
        if naziv_element:
            naziv = (naziv_element.get_text(strip=True)
                    .replace('- Dom za starije', '')
                    .replace('-Dom za starije', '')
                    .replace('- Obiteljski dom za starije', '')
                    .replace('-Obiteljski dom za starije', '')
                    .strip())
            detalji_doma['Naziv'] = naziv
            
        
        # Address
        adresa_element = soup.find('i', class_='icon ion-location')
        if adresa_element:
            parent_p_tag = adresa_element.find_parent('p')
            if parent_p_tag:
                detalji_doma['Adresa'] = parent_p_tag.get_text(strip=True).split("Prikaži lokaciju")[0].strip()

        # Telephone and other contacts
        contact_info_box = soup.find('div', class_='basic-data')
        if contact_info_box:
            telefoni = []
            tel_elementi = contact_info_box.find_all('i', class_='icon ion-ios-telephone')
            for tel_icon in tel_elementi:
                tel_text = tel_icon.find_parent('p').get_text(strip=True).replace(" ", "").replace("/", "")
                telefoni.append(tel_text)
            if telefoni:
                detalji_doma['Telefoni'] = ", ".join(telefoni)
            
            web_element = contact_info_box.find('a', href=lambda href: href and 'http' in href and not 'domovi-za-starije.com' in href and not 'facebook' in href)
            if web_element:
                detalji_doma['Web_stranica'] = web_element['href']
        
        # TODO: Fix this osnovni podatci is None
        # Other basic details
        osnovni_podaci_box = soup.find('div', class_='osnovni-podaci')
        if osnovni_podaci_box:
            fields = osnovni_podaci_box.find_all('div', class_='field')
            for field in fields:
                key_element = field.find('span', class_='field-label')
                value_element = field
                if key_element:
                    key = key_element.get_text(strip=True).replace(':', '')
                    value = value_element.get_text(strip=True).replace(key, '').replace(':', '').strip()
                    if key in detalji_doma:
                        detalji_doma[key] = value
        
        # tzpe of accommodation
        def extract_checkmark_items(container_class):
            container = soup.find('div', class_=container_class)
            if container:
                items = container.find_all('span', class_='inline')
                for item in items:
                    checkmark = item.find('i', class_='icon ion-checkmark-circled')
                    if checkmark:
                        key = item.get_text(strip=True)
                        if key in detalji_doma:
                            detalji_doma[key] = 'Da'
        extract_checkmark_items('tip-smjestaja')
        extract_checkmark_items('oblik-smjestaja')

        # services
        skrb_box = soup.find('div', class_='care')
        if skrb_box:
            rows = skrb_box.find_all('tr')
            for row in rows:
                key_element = row.find('td')
                status_element = row.find('i')
                if key_element and status_element:
                    key = key_element.get_text(strip=True).replace(':', '')
                    if key in detalji_doma:
                        if 'ion-checkmark-circled' in status_element.get('class', []):
                            detalji_doma[key] = 'Da'
                        elif 'ion-close-circled' in status_element.get('class', []):
                            detalji_doma[key] = 'Ne'
        
        # nursing services nad amenities
        oprema_doma_box = soup.find('div', class_='oprema-usluge')
        if oprema_doma_box:
            items = oprema_doma_box.find_all('span', class_='inline')
            for item in items:
                checkmark = item.find('i', class_='icon ion-checkmark-circled')
                if checkmark:
                    key = item.get_text(strip=True)
                    if key in detalji_doma:
                        detalji_doma[key] = 'Da'
        
        # Equipment of the home
        oprema_soba_box = soup.find('div', class_='opremljenost-soba')
        if oprema_soba_box:
            items = oprema_soba_box.find_all('span', class_='inline')
            for item in items:
                checkmark = item.find('i', class_='icon ion-checkmark-circled')
                if checkmark:
                    key = item.get_text(strip=True)
                    if key in detalji_doma:
                        detalji_doma[key] = 'Da'
        
        return detalji_doma
    except requests.exceptions.RequestException as e:
        print(f"Greška prilikom dohvaćanja stranice {url}: {e}")
        return None