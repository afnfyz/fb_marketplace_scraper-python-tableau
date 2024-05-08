import pandas as pd
import re
import requests 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as soup
import time

# Set up Splinter
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Set up base url
base_url = "https://www.facebook.com/marketplace/nyc/search?"
# Set up search parameters
min_price = 1000
max_price = 5000
days_listed = 1
min_mileage = 50000
max_mileage = 150000
min_year = 1998
max_year = 2020
transmission = "automatic"
make = "Honda"
model = ""
# Set up full url
url = f"{base_url}minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_listed}&maxMileage={max_mileage}&maxYear={max_year}&minMileage={min_mileage}&minYear={min_year}&transmissionType={transmission}&query={make}{model}&exact=false"

# Visit the website
driver.get(url)

# Close the popup if present
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Close"]'))).click()
except:
    pass

# Scroll down to load more results
scroll_count = 10
scroll_delay = 2

for _ in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_delay)

# Parse the HTML using BeautifulSoup from the updated page source
market_soup = soup(driver.page_source, 'html.parser')

# Initialize lists to store data
names = []
prices = []
locations = []
mileages = []
urls = []
img = []

# Extract information from each listing
listings = market_soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')  # This class contains each listing

for listing in listings:
    # Extract price
    price_element = listing.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x10flsy6 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1tu3fi x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u')
    price = price_element.text.strip() if price_element else "N/A"
    prices.append(price)

    # Extract name
    name_element = listing.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
    name = name_element.text.strip() if name_element else "N/A"
    names.append(name)

    # Extract info elements
    info_elements = listing.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft')

    # Initialize variables for location and mileage
    location = "N/A"
    mileage = "N/A"

    # Process each info element
    for info_element in info_elements:
        text = info_element.get_text(strip=True)
        if re.match(r'^[a-zA-Z,\s]+$', text):  # Match location (letters and commas)
            location = text
        elif re.match(r'^\d+\s?[Kk]?\s?miles?$', text):  # Match mileage (numbers followed by optional 'K' and 'miles')
            mileage = text

    # Append location and mileage to lists
    locations.append(location)
    mileages.append(mileage)

    # Extract URL
    url_element = listing.find('a', class_="x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 xggy1nq x1a2a7pz x1heor9g xt0b8zv x1hl2dhg x1lku1pv")
    url = url_element['href'] if url_element else "N/A"
    urls.append('https://www.facebook.com' + url)

# Create DataFrame from the lists
data = {
    'Name': names,
    'Price': prices,
    'Location': locations,
    'Mileage': mileages,
    'URL': urls
}
df = pd.DataFrame(data)

# Filter out rows where Name is "N/A"
df_filtered = df[df['Name'] != 'N/A']

# Output DataFrame to CSV
csv_filename = f'marketplace_listings.csv'
df_filtered.to_csv(csv_filename, index=False)

# Quit the webdriver
driver.quit()