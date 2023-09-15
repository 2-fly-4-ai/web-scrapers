#from transformers import pipeline
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv


#headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'}
#headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
result = requests.get(
    "https://httpbin.org/get",
    proxies={
        "http": "http://455fe7d72d1c433b99cb2cf35bb839d4:@proxy.crawlera.com:8011/",
        "https": "http://455fe7d72d1c433b99cb2cf35bb839d4:@proxy.crawlera.com:8011/",
    },
    verify='zyte-smartproxy-ca.crt' 
)

with open('spruce_petst.csv', 'w', newline='', encoding="utf-8") as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(["term","Content"])
    
    
    
df1 = pd.read_csv("the_sprucepets_sitemap_not_bgs.csv",engine = "python", error_bad_lines= False )
x = df1.values.tolist()

for i in x:
    

    URL = i[0]
    
    print(URL)
    r = requests.get(URL)

    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all(["h1","h2","h3","p"])

    results = ''.join([str(tag) for tag in results ])
    soup = BeautifulSoup(results)
    soup_object2 = soup
    #print(soup)
        
        
    for tag in soup_object2():
        for attribute in ["class","id","style","rel","data-id","target","aria-label","data-type","title",'"col-lg-8 page-content"',"col-lg-8 page-content","alt"]: # You can also add id,style,etc in the list
            tag.attrs = {}
        for a in soup_object2("a"):
            a.replaceWithChildren()
        for strong in soup_object2("strong"):
            strong.replaceWithChildren()
        for span in soup_object2("span"):
            span.replaceWithChildren()            
        for img in soup_object2("img"):
            img.decompose()
        for em in soup_object2("em"):
            em.decompose()
        for div in soup_object2("div"):
            div.decompose()
        for noscript in soup_object2("noscript"):
            noscript.decompose()
        for svg in soup_object2("svg"):
            svg.decompose()
        for figure in soup_object2("figure"):
            svg.decompose()
        for path in soup_object2("path"):
            path.decompose()
    x = ''.join([str(tag) for tag in soup_object2])

    x = x.replace("><",">$$$<")
    x = x.split("$$$")

    listx = []
    for i in x:
        if ".com" in i or "By clicking" in i or "Dotdash Meredith" in i or "Images" in i or "spruce" in i or "Spruce" in i or  i.count(".") > 8:
            i = ""
        listx.append(i)
    else:
        listx.append(i)

    x = "".join(listx)
    print(x)
#results2 = soup.find_all('h3')
#text = [result for result in results]
#print(text)
#ARTICLE = ' '.join(text)
#soup_object2 = soup
    with open('spruce_petst.csv', 'a+', newline='', encoding="utf-16") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([URL, x])

    

#text = [result.text for result in results]
#ARTICLE = ' '.join(text)
print(x)