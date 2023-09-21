from re import I
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

with open('task_purpose_dataset_bgs.csv', 'w', newline='', encoding="utf-8") as csvfile:
    #creating a csv writer object
    csvwriter = csv.writer(csvfile)
    #writing the fields
    csvwriter.writerow(["Title","Term","URL","Types","What to consider","Benefits","Pricing","Pricing Hidden(use if pricing missing)","How we chose","Key Features","Tips"])
    
df1 = pd.read_csv("taskandpurpose.com-gear-top-pages-path-all-2__2022-08-19_10-56-33.csv",engine = "python", error_bad_lines= False )
df1 = df1
df1 = df1
x = df1.URL.tolist()

for i in x:

    URL = i
    Term = URL.split("best-")[-1].replace("-"," ").replace("/","")
    ##print(Term)
    r = requests.get(URL)

    soup = BeautifulSoup(r.text, 'html.parser')
    
    title = soup.find_all(["h1"])
    title = title[0]
    #print(title[0])
    title = str(title)
    title_soup = BeautifulSoup(title)
    
    for tag in title_soup():
        for h1tag in title_soup("h1"):
            h1tag.replaceWithChildren()
            
    
    
    title_soup = str(title_soup)
    print(title_soup)
    soup_object = soup.find_all(class_=['Article-bodyText'])

    try:
        soup_object = soup_object[0].find_all(["h1","h2","h3","p","ul"])
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
        #for div in soup_object("div"):
            #div.decompose()
        for noscript in soup_object("noscript"):
            noscript.decompose()
        for svg in soup_object("svg"):
            svg.decompose()
        for figure in soup_object("figure"):
            svg.decompose()
        for path in soup_object("path"):
            path.decompose()

    soup_object = ''.join([str(tag) for tag in soup_object])
    
    types = ""
    what_to_consider = ""
    benefits = ""
    pricing = ""
    how_we_chose = ""
    methodology = ""
    tips = ""
    verdict = ""
    key_features = ""
    pricing_hidden = ""
    #"Types","What to consider","Benefits","Pricing","How we chose","Methodology"
    ##print(soup_object)
    #soup_object = soup_object.replace("<h2>Types","$$$<h2>Types").split("$$$")[-1]
    soup_object1 = soup_object.replace("<h2>","$$$<h2>").split("$$$")
    
    soup_object_find_h3 = soup_object.replace("<h2>","$$$<h2>").replace("<h3>","$$$<h3>").split("$$$")
    #for x in soup_object_find_h3:
        #if "h3" in x:
            #pricing = x
            #if "pricing" or "Pricing" or "Price" or "price" in pricing:
                #pricing = x
        #else:
            #pricing = ""
    
        
    for i in soup_object1:
        if "<h2>Types" in i or "<h2>Popular types" in i or "<h2>The most common" in i:
            #print("Types: "+i + "\n")
            types = i
            
        if "<h2>What to consider" in i or "<h2>What to look" in i or "<h2>Things to consider" in i:
            #print("Key features "+i+ "\n")
            what_to_consider = i
            
        if "<h2>Benefits" in i or "<h2>Do you need" in i or "<h2>The advantages" in i or "<h2>Benifits of" in i:
            #print("Benefits " +i+ "\n")
            benefits = i
            
        if "<h2>Pricing" in i or "pricing</h2>" in i:
            #print("Pricing "+i+ "\n")
            pricing = i
        
        if "pricing" in i and "h2" in i:
            pricing2 = i
            #print("Pricing "+i+ "\n")
            #pricing_hidden = i
            if "<h3>Pricing" in pricing2:
                pricing_hidden = pricing2.replace("<h3>Pricing","$$$<h3>Pricing").split("$$$")[-1]
                
            else:
                pricing_hidden = f"{i}"
                
                    
            
        if "<h2>How we chose" in i or "<h2>Methodology" in i:
            #print(i+ "\n")
            
            how_we_chose = i
            how_we_chose = how_we_chose.replace("<h3>","$$$<h3>").split("$$$")[0]
            
            
    
            
        if "<h2>Tips" in i:
            #print(i+ "\n")
            tips = i
                
        if "<h2>Our verdict" in i :
            #print(i+ "\n")
            verdict = i
         
        if "<h2>Key features" in i:
             key_features = i
    print(pricing)
    with open('task_purpose_dataset_bgs.csv', 'a+', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([title_soup,Term,URL,types,what_to_consider,benefits,pricing,pricing_hidden,how_we_chose,key_features,tips])
        #if "<h2>Why should you trust" in i or :
            ##print(i+ "\n")
            
    ##print(soup_object)
    ##print(soup_object)
    
    #FAQ_list = []
   
    #if "FAQs" in soup_object:
        ##print("OKay")
    #else:
        #continue
            
    #FAQ_list = soup_object
    #FAQ_list = FAQ_list.replace("<h2>","$$$<h2>").split("$$$")
    
    #faq_list_1 = []
    #for i in FAQ_list:
        #if "FAQ" in i:
             #faq_list_1.append(i)
        #else:
            #continue
            
    #FAQ_list = "".join(faq_list_1)
    
    #[-1].replace("><",">$$$<").split("$$$")
    
    
    
    #FAQ_list = FAQ_list.replace("><",">$$$<").split("$$$")
    
    #newlist_x = []
    #for i in FAQ_list:
        #if "Task" in i and "Purpose" in i:
            #i = ""
            #newlist_x.append(i)
        #else:
            #newlist_x.append(i)
            
            #.replace("<h1>","$$$<h1>").replace("<h2>","$$$<h2>").replace("<h3>","$$$<h3>").replace("<div>","$$$<div>").replace("<script>","$$$<script>")
    #soup_object = soup_object.split("$$$")[0].replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
    #intro = soup_object
    #newlist_x = "".join(newlist_x)
    ##print(newlist_x)
    ##print(newlist_x)
    
    

   