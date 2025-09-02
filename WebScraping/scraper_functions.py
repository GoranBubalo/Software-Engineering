# scraper_functions.py
import requests
from bs4 import BeautifulSoup
import re

def scrape_dom_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # AŽURIRANI PREDLOŽAK SA ŠIRIM KATEGORIJAMA
        detalji_doma = {
            'URL': url,
            'Naziv': '',
            'Adresa': '',
            'Telefoni': '',
            'Osnivac': '',
            'Ravnateljica': '',
            'Tip Smjestaja': '',
            'Oblik smjestaja': '',
            'Skrb i njega': '',
            'Opremljenost i usluge doma': '',
            'Opremljenost soba': ''
        }


        # Name
        naziv_element = soup.find('h1', class_='entry-title dom-title')
        if naziv_element:
            naziv = naziv_element.get_text()
            naziv = naziv.replace('- Dom za starije', '')
            naziv = naziv.replace('-Dom za starije', '')
            naziv = naziv.replace('- Obiteljski dom za starije', '')
            naziv = naziv.replace('-Obiteljski dom za starije', '')
            detalji_doma['Naziv'] = " ".join(naziv.strip().split())

        # Adresa
        adresa_element = soup.find('i', class_='icon ion-location')
        if adresa_element:
            parent_p_tag = adresa_element.find_parent('p')
            if parent_p_tag:
                detalji_doma['Adresa'] = parent_p_tag.get_text(strip=True).split("Prikaži lokaciju")[0].strip()

        # TODO: Change the logic 
        contact_info_box = soup.find('div', class_='basic-data')
        if contact_info_box:
            telefoni = []
            tel_elementi = contact_info_box.find_all('i', class_='icon ion-ios-telephone')
            for tel_icon in tel_elementi:
                parent_p = tel_icon.find_parent('p')
                if parent_p:
                    tel_text = parent_p.get_text(strip=True)
                    # Pronalazi sve nizove znamenki
                    brojevi = re.findall(r'\d+', tel_text)
                    if brojevi:
                        # Spaja sve pronađene nizove u jedan string bez razmaka
                        clean_number = "".join(brojevi)
                        telefoni.append(clean_number)
            if telefoni:
                detalji_doma['Telefoni'] = ", ".join(telefoni)

        # TODO: Change the logic for getting Name of the director and founder
        osnovni_podaci_box = soup.find('div', class_='card-header', string='Osnovni podaci')
        if osnovni_podaci_box:
            card_body = osnovni_podaci_box.find_next_sibling('div', class_='card-body')
            if card_body:
                fields = card_body.find_all('div', class_='field')
                for field in fields:
                    key_element = field.find('span', class_='field-label')
                    if key_element:
                        # Dohvati tekst oznake i očisti ga
                        key = key_element.get_text(strip=True).replace(':', '')
                        
                        # Ukloni element 'span' iz HTML-a
                        key_element.extract()
                        
                        # Sada dohvati preostali tekst iz 'div' taga.
                        # To će biti samo vrijednost koju tražimo.
                        value = field.get_text(strip=True)
                        
                        if key in detalji_doma:
                            detalji_doma[key] = value

        # Tip smještaja i oblik smještaja (NOVA LOGIKA)
        tip_smjestaja_items = []
        oblik_smjestaja_items = []
        
        def extract_checkmark_items_to_list(container_header_text, target_list):
            container_header = soup.find('div', class_='card-header', string=container_header_text)
            if container_header:
                container = container_header.find_next_sibling('div', class_='card-body')
                if container:
                    items = container.find_all('span', class_='inline')
                    for item in items:
                        checkmark = item.find('i', class_='icon ion-checkmark-circled')
                        if checkmark:
                            target_list.append(item.get_text(strip=True))
        
        extract_checkmark_items_to_list('Tip smještaja', tip_smjestaja_items)
        extract_checkmark_items_to_list('Oblik smještaja', oblik_smjestaja_items)

        detalji_doma['Tip Smjestaja'] = ", ".join(tip_smjestaja_items)
        detalji_doma['Oblik smjestaja'] = ", ".join(oblik_smjestaja_items)


        # Skrb i njega (maybe change logic => remove the yes and no)
        skrb_box = soup.find('div', class_='care')
        if skrb_box:
            rows = skrb_box.find_all('tr')
            skrb_i_njega_statusi = []
            for row in rows:
                key_element = row.find('td')
                status_element = row.find('i')
                if key_element and status_element:
                    key = key_element.get_text(strip=True).replace(':', '')
                    status = ''
                    if 'ion-checkmark-circled' in status_element.get('class', []):
                        status = 'Da'
                    elif 'ion-close-circled' in status_element.get('class', []):
                        status = 'Ne'
                    
                    if status:
                        skrb_i_njega_statusi.append(f"{key}: {status}")

            detalji_doma['Skrb i njega'] = ", ".join(skrb_i_njega_statusi)


        # Opremljenost i usluge doma (NOVA LOGIKA)
        oprema_doma_items = []
        oprema_doma_header = soup.find('div', class_='card-header', string='Opremljenost i usluge doma')
        if oprema_doma_header:
            container = oprema_doma_header.find_next_sibling('div', class_='card-body')
            if container:
                items = container.find_all('span', class_='inline')
                for item in items:
                    checkmark = item.find('i', class_='icon ion-checkmark-circled')
                    if checkmark:
                        oprema_doma_items.append(item.get_text(strip=True))

        detalji_doma['Opremljenost i usluge doma'] = ", ".join(oprema_doma_items)

        # Opremljenost soba (NOVA LOGIKA)
        oprema_soba_items = []
        oprema_soba_header = soup.find('div', class_='card-header', string='Opremljenost soba')
        if oprema_soba_header:
            container = oprema_soba_header.find_next_sibling('div', class_='card-body')
            if container:
                items = container.find_all('span', class_='inline')
                for item in items:
                    checkmark = item.find('i', class_='icon ion-checkmark-circled')
                    if checkmark:
                        oprema_soba_items.append(item.get_text(strip=True))
                        
        detalji_doma['Opremljenost soba'] = ", ".join(oprema_soba_items)
        
        return detalji_doma

    except requests.exceptions.RequestException as e:
        print(f"Greška prilikom dohvaćanja stranice {url}: {e}")
        return None