# Import necessary libraries
import requests
import time
from collections import Counter
from nltk.util import ngrams 
import bs4
from collections import Counter
import csv
from time import sleep
from random import randint
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize a WebDriver instance for Chrome with headless mode
driver = webdriver.Chrome()
chrome_options = Options()
chrome_options.add_argument("--headless")

result = requests.get(
    "https://httpbin.org/get",
    proxies={
        "http": "http://455fe7d72d1c433b99cb2cf35bb839d4:@proxy.crawlera.com:8011/",
        "https": "http://455fe7d72d1c433b99cb2cf35bb839d4:@proxy.crawlera.com:8011/",
    },
    verify='zyte-smartproxy-ca.crt' 
)

# Open a CSV file for writing data
with open('output.csv', 'w', newline='', encoding="utf-8") as csvfile: 
    # Create a CSV writer object 
    csvwriter = csv.writer(csvfile) 
        
    # Write the header row to the CSV
    csvwriter.writerow(["Keyword","SV","Count","Result"])

# Read data from a CSV file into a DataFrame
import pandas as pd
url = 'input.csv'
df1 = pd.read_csv(url)

# Iterate over the rows in the DataFrame
for Keyword, SV, Count in zip(df1['Keyword'], df1['SV'], df1['Count']):
    print(Keyword)
    TERM = str(Keyword)
    
    # Construct a Google search URL with a customized keyword
    url = 'https://google.com/search?q=' + "geeksforgeeks"
    print(url)

    # Fetch the URL data using requests.get(url)
    MAX_RETRY = 100
    retries = 0
    
    try:
        r = result.get(url)
        print(r)
        soup = BeautifulSoup(r.text, 'html.parser')
    except Exception as exception:
        if retries <= MAX_RETRY:
            print("ERROR=Method failed. Retrying ... #%s", retries)
            time.sleep(1) 
            continue
        else:
            raise Exception(exception)

    # Extract headings from the webpage
    try:
        heading_object1 = soup.find_all("h1")
        time.sleep(0.01)
        heading_object2 = soup.find_all("h2")
        time.sleep(0.01)
        heading_object3 = soup.find_all("h3")
        time.sleep(0.01)
        heading_object4 = soup.find_all("p")
        time.sleep(0.01)
    except:
        continue

    # Concatenate all extracted text
    all_words = ""
    for info in heading_object1:
        all_words += info.getText()
    for info in heading_object2:
        all_words += info.getText()
    for info in heading_object3:
        all_words += info.getText()
    for info in heading_object4:
        all_words += info.getText()

    # Clean the text
    all_words = all_words.replace("-", " ").replace("|", " ").replace(",", " ").replace("[", " ").replace("]", " ").replace(":", " ").lower()

    # Define a blacklist of words to exclude
    BLACKLIST = [
        # ... (add your blacklist words here)
    ]
    
    # Remove words from the blacklist
    all_words_list = all_words.split()
    deleteAsk = []
    for i in all_words_list:
        if i[0:3] == "ask" or i[0:3] == "web":
            del i
        else:
            deleteAsk.append(i)
    
    newray = []
    for i in deleteAsk:
        if len(i) > 3:
            newray.append(i)
    
    cleanlist = [word for word in newray if word not in BLACKLIST]

    # Define another blacklist
    BLACKLIST2 = [
        # ... (add more words to exclude)
    ]

    # Remove words from the second blacklist
    cleanlist = [word for word in cleanlist if not any(bad in word for bad in BLACKLIST2)]

    # Count word occurrences and extract the most common
    counts = Counter(cleanlist)
    context = counts.most_common(5)

    # Prepare n-grams
    forngrams = " ".join(cleanlist)
    n_gram = 2
    counts2 = Counter(ngrams(forngrams.split(), n_gram))
    context2 = counts2.most_common(5)

    try:
        # Extract a result from n-grams
        Result = context2[0][0][0] + " " + context2[0][0][1] + ", " + context2[1][0][0] + " " + context2[1][0][1] + ", " + context2[2][0][0] + " " + context2[2][0][1] + ", " + context2[3][0][0] + " " + context2[3][0][1] + ", " + context2[4][0][0] + " " + context2[4][0][1]
    except:
        continue

    print(context)
    
    # Write data to the CSV file
    with open('output.csv', 'a+', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([Keyword, SV, Count, Result])
