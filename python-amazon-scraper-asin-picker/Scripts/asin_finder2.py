import pandas as pd
import csv
from pathlib import Path
import sys

with open('leggings.csv', 'w',newline='' , encoding="utf-8") as csvfile:  
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Keyword","ASINs"])

source_files2 = sorted(Path('test_folder_508').glob('*.csv'))

for file in source_files2:
    
    df1 = pd.read_csv(file, encoding = "utf8", error_bad_lines = False )
    asin_list2 = []
    
    term_x = df1["search_term"].iloc[1]
    term_x = term_x.split(" ")

    term_list = []
    for i in term_x:
        i = i.capitalize()
        term_list.append(i)

    term_x = " ".join(term_list)
    
    for amazon_search_url,asin,currency,discount_pct,image_urls,images,name,num_of_ratings,price,search_term,search_term_id,star_rating,url in zip(df1["amazon_search_url"],df1["asin"],df1["currency"],df1["discount_pct"],df1["image_urls"],df1["images"],df1["name"],df1["num_of_ratings"],df1["price"],df1["search_term"],df1["search_term_id"],df1["star_rating"],df1["url"]):
        asin_list2.append(asin)


    asin_list2 = ",".join(str(x) for x in asin_list2)
    with open('leggings.csv', 'a+', newline='', encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([term_x,asin_list2])


