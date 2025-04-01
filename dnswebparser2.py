import requests
from bs4 import BeautifulSoup
import json

# URL of the website to scrape
url = "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns"

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content of the website
soup = BeautifulSoup(response.content, 'html.parser')

# Find all h2 elements and their corresponding tables starting from "Commercial" to "China"
data = {}
start_scraping = False

for h2 in soup.find_all('h2'):
    if h2.text.strip() == "Commercial":
        start_scraping = True
    if start_scraping:
        table = h2.find_next('table')
        if table:
            # Extract table data
            table_data = []
            for row in table.find_all('tr'):
                row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                table_data.append(row_data)
            # Add h2 value and table data to the dictionary
            data[h2.text.strip()] = table_data
    if h2.text.strip() == "China":
        table = h2.find_next('table')
        if table:
            # Extract table data
            table_data = []
            for row in table.find_all('tr'):
                row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                table_data.append(row_data)
            # Add h2 value and table data to the dictionary
            data[h2.text.strip()] = table_data
        break

# Convert the dictionary to JSON format
json_data = json.dumps(data, indent=4)

# Save the JSON data to a file
with open('scraped_tables.json', 'w') as f:
    f.write(json_data)

print("The tables have been scraped and saved to scraped_tables.json file.")

