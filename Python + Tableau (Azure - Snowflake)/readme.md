## Exploring Apartment Advertisements in Warsaw

Just as a farmer carefully selects the most fertile land for planting crops, real estate professionals must identify the most promising locations for property investments. 
As in agriculture, where the growth of crops necessitates diligent care and timely harvests, the growth of a real estate portfolio demands a proactive approach, seizing opportunities and nurturing investments for continued success.

This project addresses this challenge by leveraging data extraction methods to support the real estate market needs and provide insights into the most suitable locations for agencies to expand their portfolios. Through data-driven visuals, this endeavor strives to provide real estate agencies with valuable insights and recommendations regarding optimal locations for portfolio expansion within the city limits of Warsaw.

## Process Archtecture

![gif](https://github.com/rusinmt/portfolio/assets/143091357/aaff7b14-2479-43d8-8d0c-377eb57629a6)

Python takes the lead in extracting comprehensive information about flats available for sale in Warsaw, focusing on critical factors like price, area, room count, and price per square meter. Through exploratory data analysis, it delves deeper into the dataset, enhancing our understanding. Upon initial contact with the data, it's thoughtfully exported to a JSON file format. An Azure Blob Storage Container is established in the Azure cloud environment to house the dataset, and then it seamlessly transitions with Azure Data Factory, creating a connection into the Snowflake Warehouse. SQL queries are applied to prepare the data for advanced analysis. Tableau steps in to bring the insights to life, allowing for the creation of dynamic dashboard. Geospatial analysis provides a district-level perspective on property locations, price trends, room distribution, and price per square meter insights. Equipped with these findings, real estate professionals can make informed decisions to navigate the market effectively.

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
The 'User-Agent' header will mimic the Mozilla browser, which will help prevent websites from blocking or restricting access. The code will attempt to open and read a URL using functions from the 'urllib.request' library, with a 10-second timeout to abandon the request and raise an exception that will print an error message. The HTML content of the page is retrieved and parsed using BeautifulSoup, which will assist in locating specific elements by class and title.
