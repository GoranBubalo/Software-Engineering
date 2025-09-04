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
<<<<<<< HEAD
            naziv = naziv_element.get_text()
            naziv = naziv.replace('- Dom za starije', '')
            naziv = naziv.replace('-Dom za starije', '')
            naziv = naziv.replace('- Obiteljski dom za starije', '')
            naziv = naziv.replace('-Obiteljski dom za starije', '')
            detalji_doma['Naziv'] = " ".join(naziv.strip().split())

=======
            naziv = (naziv_element.get_text(strip=True)
                    .replace('- Dom za starije', '')
                    .replace('-Dom za starije', '')
                    .replace('- Obiteljski dom za starije', '')
                    .replace('-Obiteljski dom za starije', '')
                    .strip())
            detalji_doma['Naziv'] = naziv
            
        
        # Address
>>>>>>> 6e34987b1ec89d14aae9b552d65345bf0203069a
        adresa_element = soup.find('i', class_='icon ion-location')
        if adresa_element:
            parent_p_tag = adresa_element.find_parent('p')
            if parent_p_tag:
                detalji_doma['Adresa'] = parent_p_tag.get_text(strip=True).split("Prikaži lokaciju")[0].strip()

        contact_info_box = soup.find('div', class_='basic-data')
<<<<<<< HEAD
=======
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
>>>>>>> 6e34987b1ec89d14aae9b552d65345bf0203069a

        telefoni = []  # uvijek definiramo listu

        if contact_info_box:
            tel_elementi = contact_info_box.find_all('i', class_='icon ion-ios-telephone')
            
            for tel_icon in tel_elementi:
                parent_p = tel_icon.find_parent('p')
                if parent_p:
                    tel_text = parent_p.get_text(strip=True)
                    
                    # Hvata sve brojeve telefona
                    brojevi = re.findall(r'\+?\d[\d\s/-]{4,}\d', tel_text)
                    
                    if brojevi:
                        # Dodaj sve pronađene brojeve u listu
                        telefoni.extend(brojevi)

        # Ako ima brojeva, spoji ih u string, inače stavi None
        if telefoni:
            detalji_doma['Telefoni'] = ", ".join(telefoni)
        else:
            detalji_doma['Telefoni'] = None

        
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


        # Opremljenost i usluge doma TODO: (NOVA LOGIKA => add null value fro empty fields)
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