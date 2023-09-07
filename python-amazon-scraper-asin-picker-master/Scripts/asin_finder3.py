#FRANICIS NOTE THAT THIS IS DEPRECIATED. LEFTOVERS SHOULD ONLY BE CALCULATED @ THE END


import pandas as pd
import csv
from list import modifier_list
from list import brand_list
from pathlib import Path
import sys

doc1 = "keywords.csv"
doc2 = "test_x6.csv"

pd1 = pd.read_csv(doc1, engine="python", error_bad_lines = False)
pd2 = pd.read_csv(doc2, engine="python", error_bad_lines = False)


list_1 = pd1["Keyword"].astype(str).to_list()
list_2 = pd2["Keyword"].astype(str).to_list()

list_1_x = []
list_2_x = []

for i in list_1:
    i = i.lower()
    list_1_x.append(i)

for i in list_2:
    i = i.lower()
    list_2_x.append(i)

leftovers = set(list_1_x) - set(list_2_x)

leftovers_list = []

for i in leftovers:
    capitalized_terms_list = []
    x_list = i.split(" ")
    for i in x_list:
        i = i.capitalize()
        capitalized_terms_list.append(i)

    y = " ".join(capitalized_terms_list)
    leftovers_list.append(y)

df_x = pd.DataFrame(leftovers_list,
                     columns = ['Keyword'])

df_x.to_csv("leftoversx6.csv")