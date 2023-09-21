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

with open('task_purpose_dataset_intro.csv', 'w', newline='', encoding="utf-8") as csvfile:
    #creating a csv writer object
    csvwriter = csv.writer(csvfile)
    #writing the fields
    csvwriter.writerow(["TERM","INTRO"])
    
df1 = pd.read_csv("taskandpurpose.com-gear-top-pages-path-all-2__2022-08-19_10-56-33.csv",engine = "python", error_bad_lines= False )
x = df1.URL.tolist()

for i in x:

    URL = i
    Term = URL.split("best-")[-1].replace("-"," ").replace("/","")
    print(Term)
    r = requests.get(URL)

    soup = BeautifulSoup(r.text, 'html.parser')
    soup_object = soup.find_all(class_=['Article-bodyText'])

    try:
        soup_object = soup_object[0].find_all(["h1","h2","h3","p"])
    except:
        continue
    soup_object = ''.join([str(tag) for tag in soup_object])
    soup_object  = BeautifulSoup(soup_object)
    for tag in soup_object():
        for attribute in ["class","id","style","rel","data-id","target","aria-label","data-type","title",'"col-lg-8 page-content"',"col-lg-8 page-content","alt"]: # You can also add id,style,etc in the list
            tag.attrs = {}
        for a in soup_object("a"):
            a.replaceWithChildren()
        for strong in soup_object("strong"):
            strong.replaceWithChildren()
        for span in soup_object("span"):
            span.replaceWithChildren()            
        for img in soup_object("img"):
            img.decompose()
        for em in soup_object("em"):
            em.replaceWithChildren()
        for div in soup_object("div"):
            div.decompose()
        for noscript in soup_object("noscript"):
            noscript.decompose()
        for svg in soup_object("svg"):
            svg.decompose()
        for figure in soup_object("figure"):
            svg.decompose()
        for path in soup_object("path"):
            path.decompose()

    soup_object = ''.join([str(tag) for tag in soup_object])
    soup_object = soup_object.replace("<h1>","$$$<h1>").replace("<h2>","$$$<h2>").replace("<h3>","$$$<h3>").replace("<div>","$$$<div>").replace("<script>","$$$<script>")
    soup_object = soup_object.split("$$$")[0].replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
    intro = soup_object


    print(soup_object)
    
    

    with open('task_purpose_dataset_intro.csv', 'a+', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([Term, intro])

    


        