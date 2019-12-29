import pandas as pd
import urllib
import urllib.parse
import requests
import json
import numpy as np
import pyexcel as pe
from pandas import ExcelWriter
from pandas import ExcelFile
from urllib.parse import urljoin
from urllib.parse import parse_qs

df = pd.read_excel('../datasets/Tripadvisor Review Part1.xlsx')

# read in dataframe with parse_cols
# use a list to read in specific columns, even if only one column
# use 1 instead of 2 since Python is zero indexed


#df = df.loc[df ['Hotel Address'].isnull(), :]
df = df['Hotel Address']
#filtered_df = df[df['Hotel Address'].notnull()]
#df.dropna(subset=['Hotel Address'], inplace=True)
#print(df)
#sheet = pe.Sheet([df['Hotel Address']])
# filter empty
#neededColumn['Hotel Address'].replace('', np.nan, inplace=True)
#neededColumn2 = urllib.parse.urlencode(neededColumn)
#print(neededColumn2)
#print(df['Hotel Address'])

# filter empty
#neededColumn['Hotel Address'].replace('', np.nan, inplace=True)
#neededColumn.dropna(subset=['Hotel Address'], inplace=True)


#neededColumn = neededColumn.drop(neededColumn.index[neededColumn.eq('')]) #drop all null rows

#neededColumn = neededColumn.drop(neededColumn.columns[neededColumn.eq('')]) #drop all null columns

#def filter_row(row_index, row):
#        result = [element for element in row if element != '']
#        return len(result)==0

#del sheet.row[filter_row]
#sheet
#print(sheet)

# First get the each needed rows and print it

for neededColumnrow in df:
        if neededColumnrow != '':
#                print("empty list")
#        else:
#                print("list is not empty")

    #if neededColumnrow != '':

#value = 0
#    if ' ' in neededColumnrow:
#        value -= neededColumnrow
#    return value
# Encode the URL

                encodedURL = urllib.parse.quote_plus(str(neededColumnrow))
#    encodedURL = urllib.parse.quote_from_bytes(neededColumnrow)
#                print(encodedURL)

# API call
# https://nominatim.openstreetmap.org/search?q=153+Hammersmith+Road,+london &format=xml&polygon=1&addressdetails=0
# https://nominatim.openstreetmap.org/         50+Norfolk+Square &format=xml&polygon=1&addressdetails=0
                baseUrl = 'https://nominatim.openstreetmap.org'
                suffix =  '/search?q=' + encodedURL + '&format=xml&polygon=1&addressdetails=0'
#for newApiUrl in encodedURL:
#addition = encodedURL
#print(addition)
#url = urljoin(baseUrl, encodedURL)
#print(url)

#def get_url(self, word: str):

#    suffix = []
#    antonyms = []


                api = urljoin(baseUrl, suffix)
#                print(api)
 #   return suffix

#print(get_url())

# make an api call
# testing first with 1 api requests
r = requests.get('https://nominatim.openstreetmap.org/search?q=153+Hammersmith+Road,+london &format=json&polygon=1&addressdetails=0')
#print(r.json())
#r.json()

result = r.json()
jsonData = []

for data in result:
    lattitude = data['lat']
    longitude = data['lon']
    jsonData.append(lattitude)
    jsonData.append(longitude)

print(jsonData)