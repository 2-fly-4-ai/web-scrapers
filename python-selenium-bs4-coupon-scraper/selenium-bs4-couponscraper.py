# Import necessary libraries
import bleach
import pandas as pd
import re
from bs4 import BeautifulSoup
import csv
import numpy as np
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize a WebDriver instance for Chrome with headless mode
driver = webdriver.Chrome()
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Open a CSV file for writing data
with open('output.csv', 'w', newline='', encoding="utf-8") as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)

    # Write the header row to the CSV
    csvwriter.writerow(["Company","URL","Content"])

# Define the URL source
url = 'coupons-lickdeals-net.csv'

# Read the data from the CSV file into a DataFrame
df = pd.read_csv(url, encoding="utf-8", engine="python", error_bad_lines=False)
df = df

# Iterate over URLs in the DataFrame
for a in zip(df["URL"]):
    URL = a[0]
    
    # Create a range of page numbers
    pages = np.arange(1, 3, 1)
    data = []
    page = URL
    driver.get(page)
    sleep(randint(2, 10))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the heading from the URL
    URL_for_heading = URL.replace("https://coupons.slickdeals.net/","").replace("/","").capitalize()
    heading = f"<h3>About {URL_for_heading}</h3>"

    # Extract the about section from the webpage
    soup_object = soup.find_all(class_=['bp-c-panel_body'])
    soup_about = soup_object[0]
    for div in soup_about("table"):
        div.decompose()

    soup_about = soup_about.text 
    soup_about = soup_about.replace("\n","")
    soup_about = re.sub(' +',' ',soup_about).strip()
    soup_about = soup_about.replace(".",". ").replace("!","! ")
    soup_about = f"{heading}<p>{soup_about}</p>"
    print(heading+soup_about)

    # Extract the main content from the webpage
    soup_main = soup_object[1]
    for a in soup_main("a"):
        a.decompose()
    
    heading_2 = f"<h3>{URL_for_heading} Discount Tips</h3>"
    soup_main_string = str(soup_main).replace('<div class="bp-c-panel_body">','')
    soup_main_string = soup_main_string.split("<p><strong>About Slickdeals</strong></p>")
    soup_main_string = f"{heading_2} {soup_main_string[0]}"
    output = f"{soup_about}{soup_main_string}"

    # Append the data to the CSV file
    with open('output.csv', 'a+', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([URL_for_heading, URL, output])
