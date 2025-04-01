import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

def download_and_parse_tables(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    tables_data = {}

    # Find h2 headers for 'Commercial' and 'China'
    commercial_header = soup.find('h2', string='Commercial')
    china_header = soup.find('h2', string='China')
    if not commercial_header or not china_header:
        raise ValueError("Could not find the required headers 'Commercial' and 'China'")

    current_element = commercial_header.find_next('h3')
    while current_element and current_element != china_header:
        if current_element.name == 'h3':
            table_name = current_element.get_text().strip()

            # Find the next heading
            next_heading = current_element.find_next(['h3', 'h2'])
            tables_in_section = []
            sibling = current_element.next_sibling
            while sibling and sibling != next_heading:
                if getattr(sibling, 'find_all', None):
                    for possible_table in sibling.find_all('table'):
                        tables_in_section.append(possible_table)
                sibling = sibling.next_sibling

            # Parse each table
            all_rows = []
            for table in tables_in_section:
                # Replace <br> with newline
                for br in table.find_all('br'):
                    br.replace_with('\n')

                # Extract the headers
                headers = [th.get_text(separator='\n').strip() for th in table.find_all('th')]

                # Extract rows
                for row in table.find_all('tr')[1:]:
                    cells = row.find_all('td')
                    if len(cells) == len(headers):
                        row_data = {
                            headers[i]: cells[i].get_text(separator='\n').strip()
                            for i in range(len(cells))
                        }
                        # If the "Private DNS zone name" column has multiple line-separated values,
                        # split them out into separate records while preserving other column values.
                        if "Private DNS zone name" in row_data:
                            zone_values = row_data["Private DNS zone name"].splitlines()
                            # Trim out empty strings if multiple newlines appear
                            zone_values = [z.strip() for z in zone_values if z.strip()]
                            
                            if len(zone_values) > 1:
                                for zone in zone_values:
                                    new_record = row_data.copy()
                                    new_record["Private DNS zone name"] = zone
                                    all_rows.append(new_record)
                            else:
                                all_rows.append(row_data)
                        else:
                            all_rows.append(row_data)

            tables_data[table_name] = all_rows

        current_element = current_element.find_next(['h3', 'h2'])

    return tables_data

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    url = 'https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns'  # Replace with the actual URL
    tables_data = download_and_parse_tables(url)
    save_to_json(tables_data, 'tables_data.json')