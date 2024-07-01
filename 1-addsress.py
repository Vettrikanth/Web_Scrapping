from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Specify the path to the ChromeDriver executable if it's not in PATH
driver_path = 'C:/Users/DAAI/Desktop/scrapping/chromedriver.exe'  # Replace with your path to chromedriver

# Initialize the Chrome driver using the Service class
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# URL of the page to scrape
url = 'https://www.medicalis.ma/ELMOUSSAIF-Hamid/Ophtalmologue-/Rabat/Maroc/170752'

# Load the webpage
driver.get(url)

# Extract the address
address_element = driver.find_element(By.CLASS_NAME, 'adresseclient')
address = address_element.text

print(address)  # Expected output: "Adresse : Hôpital des Spécialités, Rabat"

# Clean up
driver.quit()
