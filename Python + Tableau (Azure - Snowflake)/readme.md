## Exploring Apartment Advertisements in Warsaw


Just as a farmer carefully selects the most fertile land for planting crops, real estate professionals must identify the most promising locations for property investments. 
As in agriculture, where the growth of crops necessitates diligent care and timely harvests, the growth of a real estate portfolio demands a proactive approach, seizing opportunities and nurturing investments for continued success.

This project addresses this challenge by leveraging data extraction methods to support the real estate market needs and provide insights into the most suitable locations for agencies to expand their portfolios. Through data-driven visuals, this endeavor strives to provide real estate agencies with valuable insights and recommendations regarding optimal locations for portfolio expansion within the city limits of Warsaw.


## Process Archtecture


![gif](https://github.com/rusinmt/portfolio/assets/143091357/aaff7b14-2479-43d8-8d0c-377eb57629a6)

Python takes the lead in extracting comprehensive information about flats available for sale in Warsaw, focusing on critical factors like price, area, room count, and price per square meter. Through exploratory data analysis, it delves deeper into the dataset, enhancing our understanding. Upon initial contact with the data, it's thoughtfully exported to a JSON file format. An Azure Blob Storage Container is established in the Azure cloud environment to house the dataset, and then it transitions with Azure Data Factory, creating a connection into the Snowflake Warehouse. SQL queries are applied to prepare the data for further analysis. Tableau steps in to bring the insights to life, allowing for the creation of dynamic dashboard. Geospatial analysis provides a district-level perspective on property locations, price, room distribution, and price per square meter insights. Equipped with these findings, real estate professionals can make informed decisions to navigate the market effectively.


## Webpage scraper


Starting with the setup of Python libraries,

```python
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import pandas as pd
```
and establishing the number of pages on the website.

```python
url_base = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa?distanceRadius=0&limit=72&ownerTypeSingleSelect=ALL&by=DEFAULT&direction=DESC&viewType=listing&page='
num_pages = 50

for page_num in range(1, num_pages + 1):
    url = url_base + str(page_num)
```
The scraper will go trough range from 1 to 51.

```python
headers = {'User-Agent': 'Mozilla/5.0'}
req = Request(url, headers=headers)

    try:
        response = urlopen(req, timeout=10)
        page = response.read()

        soup = BeautifulSoup(page, 'html.parser')
```
The 'User-Agent' header will mimic the Mozilla browser, which will help prevent websites from blocking or restricting access. The code will open and read a URL using functions from the 'urllib.request' library, with a 10-second timeout to abandon the request and raise an exception that will print an error message. The HTML content of the page is retrieved and parsed using BeautifulSoup, which will assist in locating specific elements by class and title.

```python
 for t, p, l, a in zip(
            soup.find_all('div', {'class': 'css-gg4vpm e1n06ry51'}),
            soup.find_all('div', {'class': 'e1jyrtvq0 css-1tjkj49 ei6hyam0'}),
            soup.find_all('p', {'class': 'css-19dkezj e1n06ry53'}),
            soup.find_all('div', {'class': 'css-70qvj9 enzg89n0'})
        ):
            data = {
                'Listing': t.text.strip(),
                'Price1': p.text.strip(),
                'Location': l.text.strip(),
                'Ads': a.text.strip(),
            }
            all_data.append(data)
```
The code is used to combine four lists representing property listing details t-itle, p-rice, l-ocation and a-dvertisement) into a single iterable. It pairs up the elements at the same index from each collection. After removing any leading or trailing whitespace from the extracted text, the data is appended to the 'all_data' list. 'Price1' will be helpful with formating the table in the next step.
```python
 print(f'Scraping page {page_num}')
```
Is used to display the progress of web scraping.
```python
divide = df['Price1'].str.split('zł', 1, expand=True)
divide.columns = ['Price', 'SQMUP1']
```
Firts 'divide' operation to split the values in column 'Price1' 
| Price1                               |
|                                 ---: |
|660 000 zł11 551 zł/m²2 pokoje57.14 m²|

Splits the DataFrame only once at the first occurrence of 'zł', hence the use of '1'. This creates two columns, 'Price' and 'SQMUP,' which stand for Square Meter Unit Price in the project.
```python
divide3 = divide2['Room Info1'].str.replace('pokój|pokoje|pokoi', 'room', regex=True).str.split('room', expand=True)
divide3.columns = ['Room Info', 'Area']
```
Another 'str.split' method uses 'str.replace' with regular expressions beforehand to find and replace substrings, affecting the 'Room Info1' column, and replaces 'pokój, pokoje, pokoi' with the word 'room', and then splits the column afterward.
```python
divide_df = pd.concat([divide, divide2, divide3], axis=1)
divide_df.drop(columns=['SQMUP1', 'Room Info1'], inplace=True)
```
Function used to concatenate three new DataFrames along the columns. After concatenation, it drops two columns.
```python
final_df = pd.concat([df, divide_df], axis=1)
final_df.drop(columns=['Price1'], inplace=True)
final_df = final_df[['Listing', 'Price', 'SQMUP', 'Room Info', 'Area', 'Location', 'Ads']]
```
To create a formatted DataFrame for further analysis, the columns are rearranged in order.


## Exploratory Data Analysis


In order to gain a deeper understanding of the characteristics, patterns, and relationships among variables, as well as to eliminate outliers from the dataset, let us proceed by installing the necessary libraries.
```python
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import json
```
Performing common preprocessing techniques for data cleaning.
```python
df = df.dropna()

df = df[[
    #'Unnamed: 0', 
    'Listing', 'Price', 'SQMUP', 'Room Info', 'Area','Location', 'Ads'
]].copy()

df = df.loc[~df.duplicated(subset=['Listing', 'Price', 'Area'])].reset_index(drop=True).copy()
```
The code eliminates rows with missing values. It then selects a subset of columns ('Listing,' 'Price,' 'SQMUP,' 'Room Info,' 'Area,' 'Location,' and 'Ads') while creating a copy of the edited DataFrame at each step to avoid any inadvertent modifications to the original data. Removes duplicate rows by applying conditions that keep only unique combinations in the 'Listing,' 'Price,' and 'Area' columns.

|-----------|---------|
| Listing   | object  |
| Price     | object  |
| SQMUP     | object  |
| Room Info | object  |
| Area      | float64 |
| Location  | object  |
| Ads       | object  |

Converting values to numeric.
