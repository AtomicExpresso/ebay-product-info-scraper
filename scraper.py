from bs4 import BeautifulSoup
import requests
import csv
import re

#Web scraper class, handels all logic
class WebScraper:
  def __init__(self, headers:list[str], url:str):
    self.headers = headers
    self.url = url
    self.table = []
    self.data = None

  #Fetch data from URL
  def req_url(self)-> None:
    print("Fetching data from url...")
    
    try:
      req = requests.get(self.url)
      soup = BeautifulSoup(req.content, 'html.parser')

      #Retreive HTML
      self.data = soup.find("div", class_="vim x-vi-evo-main-container template-evo-avip")
    except:
      raise ValueError("An error occured while fetching from url")

  #Extract text from element
  def extract_text(self, element: any, parent_type:str, class_name:str, index:int=0, prod_text:str=None) -> str:
    parent = None
    
    if prod_text:
      parent = element.find(parent_type, class_=class_name, string=(re.compile(fr"^{prod_text}")))
      print(parent)
    else:
      parent = element.find(parent_type, class_=class_name)
    
    #IF parent element exists then return its text otherwise display "n/a"
    if parent:
      find_text = parent.find_all("span")[index]
      return find_text.get_text(strip=True)
    return "n/a"

  #Scrape data from web page
  def scrap_data(self)->None:
    print("Building table of data...")

    try:
        cur_data = []

        cur_data.append([
          self.extract_text(self.data, "h1", "x-item-title__mainTitle"),#Product name
          self.extract_text(self.data, "div", "x-sellercard-atf__info__about-seller"),#Seller
          self.extract_text(self.data, "div", "x-item-condition-text", 1),#condition
          self.extract_text(self.data, "div", "x-price-primary"),#Price
          self.extract_text(self.data, "div", "ux-labels-values col-12 ux-labels-values--shipping", 1),#Shipping cost
          self.extract_text(self.data, "div", "ux-layout-section__textual-display ux-layout-section__textual-display--itemId", 1),#Item number
          self.extract_text(self.data, "div", "ux-layout-section ux-layout-section--shipping", 0, "Located in:"),#Location
        ])
        self.table.append(*cur_data)
    except:
      raise ValueError("An error occured while creating the data table, there could be an issue with the website")

  #Build CSV
  def build_csv(self) -> None:
    print("Creating CSV file...")
    try:
      with open("ebay_product.csv", 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(self.headers)
        for row in self.table:
          csv_writer.writerow(row)
      print("CSV file created with data...")

    except:
      raise ValueError("An error occured while building the csv, this could be due to a libary update, change in the website, or an issue with app permissions")

  #just used to help further simplify running code while also still being modular 
  def run_scraper(self):
    self.req_url()
    self.scrap_data()
    self.build_csv()
    print("Finished! your CSV file was created")

#Run the program
def run():
  item_id:str = ""

  #Loop for user input
  while True:
    try:
      id = int(input("What is the product ID?\nTIP: You can find this in the URL\n"))
    
      if id > 0:
        item_id = id
        break 
    except ValueError:
      print("\nMust be an integer value that's greater than 0\n")

  url:str = f"https://www.ebay.com/itm/{item_id}"
  ws = WebScraper(["Product", "Seller", "condition", "Price", "Shipping", "Item number", "Location"], url)
  ws.run_scraper()

run()