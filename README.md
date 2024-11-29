# ebay product info scraper
A basic web scraper built using the BeautifulSoup Python library. Just input a product ID, and the script will fetch details such as the product name, price, shipping cost, etc.

Note: This repository is for educational purposes only. I am not responsible for any misuse.

### Requirements
This script uses the following libaries:
- BeautifulSoup
- requests
- csv
- re

You can install all dependencies with:
```bash
pip install -r requirements.txt
```
### Usage
1. Clone the repo
   ```bash
    https://github.com/AtomicExpresso/ebay-product-info-scraper.git
   ```
2. Install the required libraries (if you havent already):
  ```bash
    pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
    python scraper.py
   ```
4. Enter the eBay product ID when prompted.
5. The scraped data will be saved to a CSV file in the current directory.
