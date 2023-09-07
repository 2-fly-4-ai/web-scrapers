import csv
from tkinter import EXCEPTION
import urllib.request
import time
import pandas as pd

count = 0
z =0



df_x = pd.DataFrame(columns=["ASIN","Title","Brands","Short description","Featured Image","Product gallery","Product categories","Status","Product AIDA","Product Features List","Product Pros & Cons","Product Url","URL Slug","Button Text","# of Reviews","Keyword Term","Amazon Canonical URL","Amazon URL Slug"])

#df1 = pd.read_csv("scoop.csv", engine= "python", error_bad_lines= False)                 
df2 = pd.read_csv("book_asins_generated (4).csv", engine= "python", error_bad_lines= False)
#df1["Keyword"] = df1["Keyword"].str.lower()
df2["Keyword"] = df2["Keyword"].str.lower()
#print(df1["term"])
####CHANGED CODE HERE
final = df2[["features","description","name","final_titles","brand","product_features","final_descriptions","image_main_url","image_gallery_urls","asin","final_adverts","final_features","final_pros_cons","amazon_urls","average_rating","url","total_ratings","term"]]
#df1 = pd.read_csv("final.csv", engine= "python", error_bad_lines= False)                 
df1 = final


for features,description,name,final_titles,brand,product_features,final_descriptions,image_main_url,image_gallery_urls,asin,final_adverts,final_features,final_pros_cons,amazon_urls,average_rating,url,total_ratings,term in zip(df1["features"],df1["description"],df1["name"],df1["final_titles"],df1["brand"],df1["product_features"],df1["final_descriptions"],df1["image_main_url"],df1["image_gallery_urls"],df1["asin"],df1["final_adverts"],df1["final_features"],df1["final_pros_cons"],df1["amazon_urls"],df1["average_rating"],df1["url"],df1["total_ratings"],df1["term"]): #,df1["Category"]
    #print(image_main_url)
    count+=1
    print(count)
    final_adverts = str(final_adverts)
    final_pros_cons = str(final_pros_cons)
    final_descriptions = str(final_descriptions)
    button_text = "Check Price"
    ###############################################################################
    ###############################################################################
    ###############################################################################
    ###############################################################################
    print(f"INPUT: {image_main_url}")
    #image_main_url = str(image_main_url).split(".")
    if "###" in str(final_features) or "###" in str(final_adverts) or "###" in str(final_pros_cons):
        continue
    
    image_main_url = image_main_url.split("._")[0]
    image_main_url = f"{image_main_url}.jpg"
    
    image_gallery_urls = str(image_gallery_urls).replace("","")
    image_gallery_urls = image_gallery_urls.split(", ")
    
    image_gallery_urls2 = []
    
    for i in image_gallery_urls:
        i = i.split("._")[0]
        i = f"{i}.jpg"
        if i == "nan.jpg":
            i = ""
        image_gallery_urls2.append(i)
        
    image_gallery_urls2 = ",".join(image_gallery_urls2)
    image_gallery_urls2 = image_gallery_urls2.replace("..", '.')
    #image_main_url2 =image_main_url2.replace("..", '.')
    ###############################################################################
    ###############################################################################
    ###############################################################################
    ###############################################################################
    
    print(f"OUTPUT: {image_main_url}")
    #print(image_gallery_urls2)
    
    amazon_urls = f"{amazon_urls}?tag=bestalternativesreview-20"
    Published = "Published"
    product_features = str(product_features).replace("{","").replace("}","").replace("'","").replace('"',"").split(",")
     
    new_features = []
    for i in product_features:
        try:
            if i[0] == " ":
                i = i[1:]
                new_features.append(i)
        except:
            i = i
            new_features.append(i)
             
    new_features = "</p><p>".join(new_features)
    new_features = f"<p>{new_features}</p>"
    #print(new_features)
    #image_main_url2 = image_main_url2.replace("..",".")
    #if image_main_url2 == "nan":
        #continue
        
        
    canonical_name = url.split(".com/")[-1].split("/")[0].replace("-"," ")
    print(f"TESTING: {canonical_name}")
    canonical_url =  url
    
    
    
        
    #############################################################  Make this part optional Or Create 2x scoops Scoop A- SCOOP-B... Scoop A needs to have this code, skip B can skip this code
    context_test = str(features)+str(description)+str(name)+str(final_titles)+str(brand)+str(product_features)+str(final_descriptions)+str(asin)+str(final_adverts)+str(final_features)+str(final_pros_cons)+str(average_rating)+str(url)+str(total_ratings)
    context_test = context_test.lower()
    term_test = term.lower()
    if term_test[-1]  == "s":
        term_test = term_test[:-1]

    context_lite = name+" "+canonical_name
    print(context_lite)
    print(term_test)
    
    ###100% Match Activator
    if term_test not in context_test:
        continue
        print("fuckup")
        
    
        #continue
    
    #############################################################
    
    
    print("\n\n\n")
    
    url = url.replace("https://www.amazon.com/","").split("/dp/")[0].split("%")[0].replace("%EF%BC%8C","").replace("--","-")
    
    z = z + 1
    #print(image_gallery_urls)
    #print("\n"*3)
    df_x.loc[z,['ASIN']] = asin
    df_x.loc[z,['Title']] = final_titles
    df_x.loc[z,['Brands']] = brand
    df_x.loc[z,['Featured Image']] = image_main_url
    df_x.loc[z,['Product gallery']] = image_gallery_urls2
    #df_x.loc[z,['Product categories']] = Category
    df_x.loc[z,['Status']] = Published
    df_x.loc[z,['Short description']] = final_descriptions
    df_x.loc[z,['Product AIDA']] = final_adverts
    df_x.loc[z,['Product Features List']] = final_features
    df_x.loc[z,['Product Pros & Cons']] = final_pros_cons
    df_x.loc[z,['Product Url']] = amazon_urls
    df_x.loc[z,['Product Rating']] = average_rating
    df_x.loc[z,['# of Reviews']] = total_ratings
    df_x.loc[z,['URL Slug']] = url
    df_x.loc[z,['Button Text']] = button_text
    df_x.loc[z,['Keyword Term']] = term
    df_x.loc[z,['Amazon Canonical URL']] = canonical_url
    df_x.loc[z,['Amazon URL Slug']] = canonical_name
      #"Amazon Canonical URL","Amazon URL Slug"  
     
    #df3.to_csv(f"/mnt/c/Users/brian/OneDrive/Desktop/scraper_zyte/test_folder_500/{file.name}")
df_x = df_x.sort_values(by="# of Reviews",ascending=False)
df_x = df_x.drop_duplicates(subset='URL Slug', keep='last')
#df_x.fillna('', inplace=True)
df_x.to_csv(f"test2.csv")
