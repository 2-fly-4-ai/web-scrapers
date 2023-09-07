import pandas as pd
import csv
from pathlib import Path
import sys
#changes to be saved

source_files = sorted(Path('scraped_folder').glob('*.csv'))
for file in source_files:

    #INITIALIZE NEW LIST
    df = pd.DataFrame(columns=["amazon_search_url","asin","currency","discount_pct","image_urls","images","name","num_of_ratings","price","search_term","search_term_id","star_rating","url","asin_score"])
    df1 = pd.read_csv(file, engine= "python", error_bad_lines=False)


    #ZERO SUM INITIALIZERS
    asin_count = 0
    countx = 0
    z =0
    number_end_asins = 0
    total_price = 0
    
    #FILES NAMES
    test = file.name
    test_name = test.replace("nan-","")
   
    #list Initializers
    dftest = []
    asin_list = []

    #CALCULATE AVERAGES
    Total = df1['price'].sum()
    num_rows = len(df1.index)

    #REMOVE WHITESPACE
    term_x = df1["search_term"].iloc[0]
    if term_x[-1] == " ":
        term_x = term_x[:-1]
    
    
    #DROP DUPES
    df1 = df1.drop_duplicates(subset="name", keep='first', inplace=False, ignore_index=False)
    for amazon_search_url,asin,currency,discount_pct,image_urls,images,name,num_of_ratings,price,search_term,search_term_id,star_rating,url in zip(df1["amazon_search_url"],df1["asin"],df1["currency"],df1["discount_pct"],df1["image_urls"],df1["images"],df1["name"],df1["num_of_ratings"],df1["price"],df1["search_term"],df1["search_term_id"],df1["star_rating"],df1["url"]):
        #INITILIALIZE LISTS
        context_list_adjusted = []

        search_term_original = search_term
        name = str(name).replace("'","").replace("-"," ").replace("é","e").lower()
        search_term = search_term.replace("'","").replace("-"," ").lower()
        url = str(url).lower()
       
       
        url_terms_split = url.replace("https://www.amazon.com/","").split("/")[0].split("-")
        name_terms_split = name.replace(")"," ").replace("("," ").replace("  "," ").split(" ")
        
        context_list = url_terms_split+ name_terms_split
        str_context_list = ' '.join(context_list)

        for i in context_list:
            i = f" {i} "
            context_list_adjusted.append(i)

        str_context_list = " ".join(context_list)
        x = ""
        search_terms_split = search_term.split(" ")
        search_terms_split = [x for x in search_terms_split if x != '']


        positive_result = 0
        positive_result_list = []

        for i in set(search_terms_split):
                        if i[-1] == "s":
                            i = i[:-1]
                        if i in str_context_list:
                            positive_result += 1
                            positive_result_list.append(str_context_list)
                                #######print(i)

        all_words_contained_check = []
        #if all_words_contained_check == True:
        true_check = 0
        false_check = 0

        for i in search_terms_split:
            
            if i[-1] == "s":
                i = i[:-1]
            i = f" {i} "
            
            str_context_list = f" {str_context_list} "
            if i in str_context_list:
                true_check += 1
            else:
                false_check += 1
            

        if true_check > 0 and false_check < 1:
            positive_result += 1000
        if positive_result < 1 :
            continue        
        if num_of_ratings < 20:
            continue
        if str(num_of_ratings) == "nan":
            continue
        if str(price) == "nan":
            continue
        if star_rating < 3.5:
            continue

        search_term_modifiers = []
        context_modifiers = []

    
        #EXACT NUMBER CHECKER
        number_list = ["1","2","3","4","5","6","7","8","9","0"]
    
        search_term_numbers = []
        name_term_numbers = []

        l1_test = False        
        for number in number_list:
            if number in search_term:
                search_term_numbers.append(number)
            if number in str_context_list:
                name_term_numbers.append(number)
            
        if search_term_numbers == name_term_numbers or positive_result > 1000:
            l1_test = False
        elif len(search_term_numbers) == 0:
            l1_test = False
        elif len(search_term_numbers) > 0 and search_term_numbers != name_term_numbers:
            ###print("FUCK")
            li_test = True

        #ASIN COUNTER        
        asin_count += 1

        #asin_list.append(asin)
        z = z + 1
        df.loc[z,['amazon_search_url']] = amazon_search_url
        df.loc[z,['asin']] = asin
        df.loc[z,['currency']] = currency
        df.loc[z,['discount_pct']] = discount_pct
        df.loc[z,['image_urls']] = image_urls
        df.loc[z,['images']] = images
        df.loc[z,['name']] = name
        df.loc[z,['num_of_ratings']] = num_of_ratings
        df.loc[z,['price']] = price
        df.loc[z,['search_term']] = search_term_original
        df.loc[z,['star_rating']] = star_rating
        df.loc[z,['url']] = url
        df.loc[z,['asin_score']] = positive_result
        
    #AVERAGES AND LIMITS
    num_rows = len(df.index)    
    Total = df['price'].sum()
    try:
        average_price_all_est = Total/num_rows
        x_limit = average_price_all_est/3
    except:
        continue
    
    df3 = df[~(df['price'] < x_limit)] 
    len_test = len(df3.index) 
    
    #SORTING
    df3 = df3.sort_values(['num_of_ratings'], ascending=[False])
    df3 = df3.sort_values(['asin_score'], ascending=[False])
    df3 = df3.head(100)
    #asin_list = ",".join(str(x) for x in asin_list)

    df3.to_csv(f"y/{test_name}")


