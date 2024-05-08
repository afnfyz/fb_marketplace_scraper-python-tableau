## Facebook Marketplace Car Scraper
This repository contains a Python script for scraping car listings from Facebook Marketplace based on specified search criteria. The script uses Selenium and BeautifulSoup to navigate the Marketplace website, extract data from listings, and store the results in a CSV file.

### Prerequisites
Before running the script, ensure you have the following installed:

**Python 3.x**

**Selenium (pip install selenium)***

**BeautifulSoup (pip install beautifulsoup4)**

**Chrome WebDriver (automatically handled by ChromeDriverManager)**

### Setup and Usage
1. Clone the repository:
``` bash
git clone https://github.com/yourusername/facebook-marketplace-scraper.git
```

2. Install dependencies:
``` bash
pip install -r requirements.txt
```
3. Run the script:
``` bash
python3 marketplace_scraper.py
```

### Parameters
**Modify the following parameters in the script to customize your search criteria:**

- min_price: Minimum price filter for listings.

- max_price: Maximum price filter for listings.

- days_listed: Number of days since the listing was posted.

- min_mileage: Minimum mileage filter for vehicles.

- max_mileage: Maximum mileage filter for vehicles.

- min_year: Minimum manufacturing year for vehicles.

- max_year: Maximum manufacturing year for vehicles.

- transmission: Transmission type (e.g., "automatic", "manual").

- make: Vehicle make (e.g., "Honda", "Toyota").

- model: Optional vehicle model (leave empty for any model).

### Notes
The script scrolls down the webpage to load more listings. 

Adjust **scroll_count** and **scroll_delay** variable in the script for desired behavior.

Make sure to update Chrome WebDriver and Chrome browser for compatibility.

Ensure compliance with Facebook's terms of service when using this script for web scraping.

### Output
The script will generate a CSV file (marketplace_listings.csv) containing the following columns:

- Name: Listing title.
- Price: Listing price.
- Location: Listing location.
- Mileage: Vehicle mileage.
- URL: URL to the listing on Facebook Marketplace.

### Tableau Dashboard
Accompanying this script is a Tableau dashboard (fb_marketplace_dashboard.twbx) that visualizes the data extracted from Facebook Marketplace. 
The dashboard includes a map, table and filters to explore the scraped car listings interactively.
Open the dashboard and connect the data to the dashboard.

![Marketplace vehicle tracker dashboard](https://github.com/afnfyz/python/assets/124072294/95222957-a36f-4995-86dc-a874db824e7e)