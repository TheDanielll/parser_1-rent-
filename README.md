# New parser for parse content and info from special site
This Python script scrapes real estate listings from the RealtyLink website and stores the data in a JSON file. It utilizes the requests library to fetch web pages, BeautifulSoup for parsing HTML, and json for handling JSON data.
# Features:
Listing Data Extraction: Parses individual real estate listings to extract relevant information such as title, address, description, price, date posted, number of rooms, area, and photo links.
Pagination Handling: Iterates through multiple pages of listings to gather a comprehensive dataset.
User-Agent Spoofing: Utilizes custom headers to mimic browser requests, ensuring smooth scraping without being blocked.
Data Storage: Writes the extracted listing data to a JSON file (listings.json) for further analysis or integration with other applications.
# How to Use:
Clone the repository: git clone [https://github.com/TheDanielll/parser_1-rent-.git](https://github.com/TheDanielll/parser_1-rent-.git)
Install dependencies: pip install -r requirements.txt
Run the script: python scrape_real_estate.py
# Dependencies:
requests: For making HTTP requests to fetch web pages.
BeautifulSoup: For parsing HTML content and extracting data from web pages.
# Notes:
The script is tailored for scraping real estate listings from RealtyLink but can be adapted for other websites with similar structure.
Adjustments may be needed for specific website layouts or changes in the HTML structure.
Feel free to contribute enhancements, report issues, or suggest improvements!
