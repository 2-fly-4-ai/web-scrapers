import pandas as pd
import csv
import sys

with open('xxxxx_test2.csv', 'a+', newline='', encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["name","price","total_ratings","image_urls","average_rating","brand","brand_url","url","asin","term","is_valid_asin","description","features","product_features","details","questions","reviews","images","Keyword","ASINs","custom_brand","ID","amazon_urls","error_images","image_gallery_urls","image_main_url"])

# DATAFRAME
url = "boxing-shorts-test - Sheet1 (1)_generated (3).csv"
df1 = pd.read_csv(url)


df = pd.DataFrame(columns=["name","price","total_ratings","image_urls","average_rating","brand","brand_url","url","asin","term","is_valid_asin","description","features","product_features","details","questions","reviews","images","Keyword","ASINs","custom_brand","ID","amazon_urls","error_images","image_gallery_urls","image_main_url"])    


#LIST INITIALIZERS
loss = 0
counter = 0

for name,price,total_ratings,image_urls,average_rating,brand,brand_url,url,asin,term,is_valid_asin,description,features,product_features,details,questions,reviews,images,Keyword,ASINs,custom_brand,ID,amazon_urls,error_images,image_gallery_urls,image_main_url in zip(df1["name"],df1["price"],df1["total_ratings"],df1["image_urls"],df1["average_rating"],df1["brand"],df1["brand_url"],df1["url"],df1["asin"],df1["term"],df1["is_valid_asin"],df1["description"],df1["features"],df1["product_features"],df1["details"],df1["questions"],df1["reviews"],df1["images"],df1["Keyword"],df1["ASINs"],df1["custom_brand"],df1["ID"],df1["amazon_urls"],df1["error_images"],df1["image_gallery_urls"],df1["image_main_url"]):
    #NUMBER INITIALIZERS
    positive_result = 0
    true_check = 0
    false_check = 0
    check_false = 0

    #NLTK STOP WORLDS
    stop_words = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their","theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was","were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and","but","if","or","because","as","until","while","of","at","by","for","with","about","against","between","into","through","during","before","after","above","below","to","from","up","down","in","out","on","off","over","under","again","further","then","once","here","there","when","where","why","how","all","any","both","each","few","more","most","other","some","such","no","nor","not","only","own","same","so","than","too","very","s","t","can","will","just","don","should","now"]
    
    #CONTEXT PREPARATION
    url_context = url.split(".com/")[1].split("/dp/")[0].replace("-"," ")
    colors = str(colors).replace("$$$"," ")#THIS IS A DEAD END FOR NOW. 
    
    context_pre = f"{name} {brand} {description} {features} {product_features} {details} {url_context}".lower().replace("$$$"," ").split(" ")
    term2 = term.lower()
    search_terms_split = term2.split(" ")
    context_pre = set(context_pre) - set(stop_words)
    context_pre = "".join(context_pre).split(" ")
    
    for i in search_terms_split:
        if i[-1] ==  "s":
            i = i[:-1]
        for x in context_pre:
            if i not in x:
                check_false += 1    
    if check_false > 0:
        loss += 1
        print(f"THIS IS THE LOSSSSSS: {loss}")
        continue
               
    with open('xxxxx_test2.csv', 'a+', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([name,price,total_ratings,image_urls,average_rating,brand,brand_url,url,asin,term,is_valid_asin,description,features,product_features,details,questions,reviews,images,Keyword,ASINs,custom_brand,ID,amazon_urls,error_images,image_gallery_urls,image_main_url])        
    