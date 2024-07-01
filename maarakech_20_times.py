import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_info(url):
    try:
        # Initialize the Chrome driver using the Service class
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Load the webpage
        driver.get(url)

        # Click on the "Afficher le Téléphone" button to reveal the phone number
        phone_button = driver.find_element(By.ID, 'telephoneFirme')
        phone_button.click()

        # Wait until the phone number is displayed
        phone_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'telephoneFirmeDisplay'))
        )

        # Extract the name
        name_element = driver.find_element(By.CLASS_NAME, 'nomprenomclient')
        name = name_element.text

        # Extract the address
        address_element = driver.find_element(By.CLASS_NAME, 'adresseclient')
        address = address_element.text

        # Extract the phone number
        phone = phone_element.text

        return name, address, phone
    except Exception as e:
        return None, None, None
    finally:
        # Clean up
        driver.quit()

# Specify the path to the ChromeDriver executable if it's not in PATH
driver_path = 'C:/Users/DAAI/Desktop/scrapping/chromedriver.exe'  # Replace with your path to chromedriver

# Set Chrome options for French language
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--lang=fr")
# chrome_options.add_argument("--headless")

# Initialize the Chrome driver using the Service class
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the page to scrape
url = 'https://www.medicalis.ma/liste?tags=Ophtalmologue+&ReferenceVille=054'

# Create and open the CSV file for writing with French encoding
csv_file_path = 'C:/Users/DAAI/Desktop/scrapping/output/marrakech_20_times.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Address', 'Phone', 'Profile URL'])

    # Refresh the page 20 times and scrape new doctor profiles each time
    for _ in range(20):
        # Load the webpage
        driver.get(url)

        # Find all the doctor links within the 'nomprenomclient' class
        doctor_links = driver.find_elements(By.CSS_SELECTOR, '.nomprenomclient a')

        # List to store profile page URLs
        profile_pages = []

        # Extract href attribute from each link and construct the profile page URL
        for link in doctor_links:
            href = link.get_attribute('href')
            if href and not href.startswith("mailto:"):
                # Correct duplicated domain part in URL
                href = href.replace('https://www.medicalis.mahttps://www.medicalis.ma', 'https://www.medicalis.ma')
                profile_pages.append(href)

        # Write the name, address, phone number, and profile URL for each profile page URL to the CSV file
        for profile_url in profile_pages:
            # Get the info for each URL
            name, address, phone = get_info(profile_url)
            if name and address and phone:
                writer.writerow([name, address, phone, profile_url])
            else:
                writer.writerow(['Unable to retrieve information', '', '', profile_url])

        # Wait for a while before refreshing the page again (to avoid spamming the server)
        time.sleep(3)

# Clean up
driver.quit()
