# Requires: requests, beautifulsoup4
import requests
from bs4 import BeautifulSoup
import json

url = "https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

data = {}
current_h2 = "Uncategorized"
current_h3 = "General"

# Iterate through elements to track current h2 and h3 categories
for element in soup.find_all(["h2", "h3", "table"]):
    if element.name == "h2":
        current_h2 = element.get_text(strip=True)
        data[current_h2] = {}
        current_h3 = "General"
    elif element.name == "h3":
        current_h3 = element.get_text(strip=True)
    elif element.name == "table":
        headers = [header.get_text(strip=True) for header in element.find_all("th")]
        rows = []
        for row in element.find_all("tr")[1:]:
            cells = [cell.get_text(separator="\n", strip=True) for cell in row.find_all("td")]
            if cells:
                row_dict = dict(zip(headers, cells))

                # Handle line breaks in "Private DNS zone name" and "Public DNS zone forwarders"
                private_dns_zones = row_dict.get("Private DNS zone name", "").splitlines()
                public_dns_forwarders = row_dict.get("Public DNS zone forwarders", "").splitlines()

                # If multiple entries exist, create separate entries for each pair
                if len(private_dns_zones) > 1 and len(private_dns_zones) == len(public_dns_forwarders):
                    for priv_dns, pub_dns in zip(private_dns_zones, public_dns_forwarders):
                        new_row = row_dict.copy()
                        new_row["Private DNS zone name"] = priv_dns
                        new_row["Public DNS zone forwarders"] = pub_dns
                        rows.append(new_row)
                else:
                    rows.append(row_dict)

        # Initialize nested dictionaries if not already present
        if current_h2 not in data:
            data[current_h2] = {}
        data[current_h2][current_h3] = rows

# Save to JSON file
with open("tables_categorized_h3.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4)

print("Data saved to tables_categorized_h3.json")