from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
url = "https://www.medicalis.ma/liste?tags=Ophtalmologue+&ReferenceVille=022"
driver.get(url)

def scrape_profiles(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    profiles = soup.find_all('div', class_='lh-content')

    for profile in profiles:
        name_elem = profile.find('p', class_='nomprenomclient')
        if name_elem:
            name = name_elem.text.strip()
        else:
            name = "Name not available"

        occupation_elem = profile.find('a', class_='linkspecialiteannonceur')
        occupation = occupation_elem.text.strip() if occupation_elem else "Occupation not available"

        address_elem = profile.find('address', class_='address.adresseclient')
        # address_elem = driver.find_element(By.CLASS_NAME, 'adresseclient')
        # address = address_elem.text
        address = address_elem.text.replace('Adresse :', '').strip() if address_elem else "Address not available"

        try:
            phone_button = driver.find_element(By.ID, 'btntel')
            driver.execute_script("arguments[0].click();", phone_button)
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'telephoneFirmeDisplay'))
            )
            phone = driver.find_element(By.ID, 'telephoneFirmeDisplay').text.strip()
        except Exception as e:
            phone = "Phone number not available"

        print(f"Name: {name}\nOccupation: {occupation}\nAddress: {address}\nPhone: {phone}\n")

refresh_count = 25

for _ in range(refresh_count):
    scrape_profiles(driver)
    driver.refresh()
    time.sleep(5)

driver.quit()