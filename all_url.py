from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Specify the path to the ChromeDriver executable if it's not in PATH
driver_path = 'C:/Users/DAAI/Desktop/scrapping/chromedriver.exe'  # Replace with your path to chromedriver

# Initialize the Chrome driver using the Service class
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service)

# URL of the page to scrape
url = 'https://www.medicalis.ma/liste?tags=Ophtalmologue+&ReferenceVille=060'

# Load the webpage
driver.get(url)

# Find all the doctor links within the 'row' class
doctor_links = driver.find_elements(By.CSS_SELECTOR, '.row a')

# List to store profile page URLs
profile_pages = []

# Extract href attribute from each link and construct the profile page URL
for link in doctor_links:
    href = link.get_attribute('href')
    if href:
        profile_url = 'https://www.medicalis.ma' + href
        profile_pages.append(profile_url)

# Print the list of profile page URLs
for profile_url in profile_pages:
    print(profile_url)

# Clean up
driver.quit()
