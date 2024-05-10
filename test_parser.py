import requests
from bs4 import BeautifulSoup
import json

#Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}

#Function to parse data from a single listing
def parse_listing(listing_url):
    #Requesting the listing URL
    response = requests.get(listing_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Selecting elements using CSS selectors
    title_elem = soup.select_one('#overview > div.row.property-tagline > div.d-none.d-sm-block.house-info > div > div.col.text-left.pl-0 > h1 > span')
    title = title_elem.text.strip() if title_elem else None

    content_elem = soup.select_one('#overview > div.row.property-tagline > div.d-none.d-sm-block.house-info > div > div.col.text-left.pl-0 > div.d-flex.mt-1 > h2')
    content = content_elem.text.strip() if content_elem else None
    if content:
        # Splitting the content into address and region
        address, region = [x.strip() for x in content.split(',')[:2]]
    else:
        address = None
        region = None

    description_elem = soup.select_one('div[itemprop="description"]')
    description = description_elem.text.strip() if description_elem else None

    date_posted_elem = soup.select_one('#overview > div.grid_3 > div.sale-row.legacy-reset > div > div.sale-title-and-data-section > div.sale-data-section > table > tbody > tr > td:nth-child(1)')
    date_posted = date_posted_elem.text.strip() if date_posted_elem else None

    price_elem = soup.select_one('.price meta[itemprop="price"]')
    price = price_elem['content'] if price_elem else None
    price_with_dollar = price + "$"

    rooms_elem = soup.select_one('.cac')
    rooms = rooms_elem.text.strip() if rooms_elem else None

    area_elem = soup.select_one('#overview > div.grid_3 > div.col-lg-12.description > div:nth-child(6) > div:nth-child(1) > div.carac-value > span')
    area = area_elem.text.strip() if area_elem else None

    photo_links = []

    primary_photo = soup.select_one('.primary-photo-container img')
    if primary_photo and 'src' in primary_photo.attrs:
        photo_links.append(primary_photo['src'])

    secondary_photos = soup.select('a', class_='secondary-photo-container')
    for photo_container in secondary_photos:
        photo = photo_container.find('img')
        if photo and 'src' in photo.attrs:
            photo_links.append(photo['src'])

    return {
        'link': listing_url,
        'title': title,
        'region': region,
        'address': address,
        'description': description,
        'date_posted': date_posted,
        'price': price_with_dollar,
        'rooms': rooms,
        'area': area,
        'photos': photo_links
    }

#Function to get listings from multiple pages
def get_listings(base_url):
    listings_data = []
    current_page = 1
    while len(listings_data) < 60:  # Limiting to 60 listings
        url = f"{base_url}&page={current_page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        listings = soup.select('.property-thumbnail-item a.property-thumbnail-summary-link')
        for listing in listings:
            if len(listings_data) >= 60:
                break
            listing_url = f"https://realtylink.org{listing['href']}"
            listing_data = parse_listing(listing_url)
            listings_data.append(listing_data)

        current_page += 1

    return listings_data

#Main URL of the listings
serp_url = 'https://realtylink.org/en/properties~for-rent?view=Thumbnail&uc=6'

#Getting listings data
listings_data = get_listings(serp_url)

#Writing data to a JSON file
with open('listings.json', 'w', encoding='utf-8') as f:
    json.dump(listings_data, f, ensure_ascii=False, indent=4)

print('JSON file successfully created.')

