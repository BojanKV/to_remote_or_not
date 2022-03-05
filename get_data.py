import requests
from bs4 import BeautifulSoup
import re
import os

def get_html(url):
    """
    :param url string
    :return: BeautifulSoup soup Object
    """

    data = requests.get(url)

    html = data.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_file(file):
    """
    :param file file to read
    :return: BeautifulSoup soup Object
    """
    htmlDoc = open(file,"r+")
    soup = BeautifulSoup(htmlDoc, 'html.parser')
    htmlDoc.close()

    return soup

def get_average_price(soup):
    """
    :param soup BeautifulSoup soup Object
    :return float average price
    """
    prices = []

    table = soup.find('table', id='price_table')

    rows = table.find_all("tr")

    for row in rows:
        data_list = row.find_all("td")
        for data in data_list:
            br_list = row.find_all("b")
            #print(br_list)
            for br in br_list:
              price_row = str(br)
              m = re.match( r'(.*>)([0-9]+,[0-9+]+).*', price_row)
              if m:
                s = m.group(2)
                s = s.replace('.','').replace(',','.')
                prices.append(float(s))

    return sum(prices)/len(prices)

# get today's diesel price

URL = "https://bensinpriser.nu/stationer/diesel/skane-lan/malmo"
soup = get_html(URL)

# calculate average price in the city

avg_diesel_f = get_average_price(soup)
avg_diesel = float('{0:.3g}'.format(avg_diesel_f))

# load page for update

local_index_filename = "index.html"

local_index = get_file(local_index_filename)

# update answer

# diesel price on day: 2020-04-21
# source: https://tanka.se/prishistorik
reference_price = 13.53

print("reference_price: {}".format(reference_price))
print("avg_diesel:      {}".format(avg_diesel))

if reference_price >= avg_diesel:
  local_index.find(id='answer').string.replace_with('NO!')
  local_index.find(id='short_explanation').string.replace_with('Diesel price is low today :)')
  print("NO")
elif (reference_price *1.4) <= avg_diesel:
  local_index.find(id='answer').string.replace_with('HELL YES!')
  local_index.find(id='short_explanation').string.replace_with('Diesel price at least 40% higher than times before corona!')
  print("HELL YES")
else:
  local_index.find(id='answer').string.replace_with('YES!')
  local_index.find(id='short_explanation').string.replace_with('Diesel price higher than times before corona')
  print("YES")

# write back new page

with open(local_index_filename, "w", encoding='utf-8') as file:
    file.write(str(local_index))
file.close()
