# Azure Private DNS Web Parser

This Python script parses the [Azure Private Endpoint DNS documentation](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns) and extracts DNS zone information categorized by cloud type (Commercial, Government, China). It outputs the data into a structured JSON file (`tables_categorized_h3.json`).

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

## Installation

Install required Python packages:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script from your terminal:

```bash
python dnswebparser3.py
```

This generates a JSON file named `tables_categorized_h3.json`.

## Web Interface

A simple HTML/JavaScript web interface (`staticwebpage.html`) is provided to:

- Load and display the parsed JSON data.
- Allow users to select cloud categories (Commercial, Government, China).
- Select nested Azure services.
- Export selected DNS zone forwarders into a single JSON file (`AzureDNSForwarders.json`).

### How to use the Web Interface

1. Ensure `staticwebpage.html` and `tables_categorized_h3.json` are in the same directory.
2. Open `staticwebpage.html` in your browser.
3. Select a cloud category and nested Azure services.
4. Click "Export Selected" to download the selected DNS forwarders as `AzureDNSForwarders.json`.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`

Install Python dependencies:

```bash
pip install requests beautifulsoup4
```

## License

This project is provided as-is without warranty. Use and modify freely.