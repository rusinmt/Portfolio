## Table of contents

- [Process Archtecture](#process-archtecture)
- [Web scraper](#web-scraper)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Setting up Azure Data Factory and Snowflake connection](#setting-up-azure-data-factory-and-snowflake-connection)

(&nbsp;)
## Exploring Apartment Advertisements in Warsaw


Just as a farmer carefully selects the most fertile land for planting crops, real estate professionals must identify the most promising locations for property investments. 
As in agriculture, where the growth of crops necessitates diligent care and timely harvests, the growth of a real estate portfolio demands a proactive approach, seizing opportunities and nurturing investments for continued success.

This project addresses this challenge by leveraging data extraction methods to support the real estate market needs and provide insights into the most suitable locations for agencies to expand their portfolios. Through data-driven visuals, this endeavor strives to provide real estate agencies with valuable insights and recommendations regarding optimal locations for portfolio expansion within the city limits of Warsaw.


## Process Archtecture


![gif](https://github.com/rusinmt/portfolio/assets/143091357/aaff7b14-2479-43d8-8d0c-377eb57629a6)

Python takes the lead in extracting comprehensive information about flats available for sale in Warsaw, focusing on critical factors like price, area, room count, and price per square meter. Through exploratory data analysis, it delves deeper into the dataset, enhancing our understanding. Upon initial contact with the data, it's thoughtfully exported to a JSON file format. An Azure Blob Storage Container is established in the Azure cloud environment to house the dataset, and then it transitions with Azure Data Factory, creating a connection into the Snowflake Warehouse. SQL queries are applied to prepare the data for further analysis. Tableau steps in to bring the insights to life, allowing for the creation of dynamic dashboard. Geospatial analysis provides a district-level perspective on property locations, price, room distribution, and price per square meter insights. Equipped with these findings, real estate professionals can make informed decisions to navigate the market effectively.


## Web scraper


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
<div align="center">

| Price1                               |
|                                 ---: |
|660 000 zł11 551 zł/m²2 pokoje57.14 m²|

</div>

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

<div align="center">
    <table>
      <tr>
        <td>Listing</td>
        <td>object</td>
      </tr>
      <tr>
        <td>Price</td>
        <td>object</td>
      </tr>
      <tr>
        <td>SQMUP</td>
        <td>object</td>
      </tr>
      <tr>
        <td>Room Info</td>
        <td>object</td>
      </tr>
      <tr>
        <td>Area</td>
        <td>float64</td>
      </tr>
      <tr>
        <td>Location</td>
        <td>object</td>
      </tr>
      <tr>
        <td>Ads</td>
        <td>object</td>
      </tr>
    </table>
</div>

Converting values to numeric.
```python
df['Price'] = pd.to_numeric(df['Price'].str.replace('[\xa0, ]', '', regex=True))

df['SQMUP'] = pd.to_numeric(df['SQMUP'].str.replace('[\xa0, ]', '', regex=True))

df['Room Info'] = pd.to_numeric(df['Room Info'].str.replace('[\xa0+,]', '', regex=True))
```
Removing non-breaking space characters and plus signs.
<div align="center">
    
|      |         Price |       SQMUP |   Room Info |        Area |
|:-----|--------------:|------------:|------------:|------------:|
| count |     3,267.000 |    3,267.000 |    3,267.000 |    3,267.000 |
| mean  | 1,976,517.784 |   16,725.794 |       2.741 |      70.558 |
| std   | 8,035,822.220 |    5,907.600 |       1.073 |     275.404 |
| min   |     224,500.000 |       36.000 |       1.000 |      13.000 |
| 25%   |     650,000.000 |   12,898.000 |       2.000 |      43.280 |
| 50%   |     835,000.000 |   15,753.000 |       3.000 |      56.100 |
| 75%   | 1,250,000.000 |   19,085.500 |       3.000 |      76.175 |
| max   | 134,602,330.000 |   75,000.000 |      10.000 | 15,650.000 |

</div>

Using df.describe() funtion to help find outliners in the data. 
```python
show5 = df['SQMUP'].nsmallest(5)
show5
```
<div align="center">
    <table>
      <tr>
        <td>1155</td>
        <td>36</td>
      </tr>
      <tr>
        <td>1099</td>
        <td>4424</td>
      </tr>
      <tr>
        <td>1333</td>
        <td>4424</td>
      </tr>
      <tr>
        <td>1724</td>
        <td>4424</td>
      </tr>
      <tr>
        <td>2018</td>
        <td>4424</td>
      </tr>
    </table>
</div>

Filtering odd values.

```python
check = df[df.index == 1155 ]
check
```
| Listing                                     | Price  | SQMUP | Room Info |   Area   | Location                                     | Ads                                 |
|---------------------------------------------|--------|-------|-----------|----------|----------------------------------------------|-------------------------------------|
| Małe mieszkanie przy Alejach Jerezolimskich | 567469 |  36   |    2      | 15650.000| al. Aleje Jerozolimskie, Stare Włochy, Włochy | NEUF Sp. z o.oBiuro nieruchomości |

```python
df = df.drop([1137, 350, 1144, 589, 558, 2185, 1476, 1384, 563, 262, 947, 1143, 1368, 1385, 683, 139, 252, 707, 3078, 710, 714, 
              779, 825, 2700, 718, 713, 3191, 1080, 2166, 1644, 1643, 2191, 2105, 948, 2115, 2112, 1985, 2122, 2123, 950, 1155])

df = df.reset_index(drop=True).copy()
```
Dropping specific rows by their Index number and reindexing the DataFrame.
```python
df['Ads'] = df['Ads'].apply(lambda x: 'Biuro nieruchomości' if 'nieruchomości' in x.lower() else x)
df['Ads'] = df['Ads'].apply(lambda x: 'Inwestycja deweloperska' if 'deweloperska' in x.lower() else x)
```
If the keywords 'nieruchomości' or 'deweloperska' are present in the text, they are replaced with new labels, otherwise, they remain the same.
```python
sns.pairplot(df, vars=['Price', 'SQMUP', 'Room Info', 'Area'], hue='Ads')

plt.show()
```

![pairplot](https://github.com/rusinmt/portfolio/assets/143091357/2932688d-097c-4a9c-8655-8059c85dfc6f)

This code utilizes Seaborn's pairplot function to create a pairwise scatterplot matrix. It visualizes how these numeric variables relate to each other within different categories of 'Ads'. The only strong correlation is an obvious one, between the number of rooms in 'Room Info' and the Area. This positive correlation suggests that apartments with more rooms tend to have a larger area.

<p align="center">
  <img src="https://github.com/rusinmt/portfolio/assets/143091357/433d0a8e-ac90-4fea-80c2-ea184b95275c">
</p>

There is a very weak but visible correlation between Price and Area or SQMUP and the Area. When the size of the apartment increases, the prices tend to slightly increase.
```python
districts = [
    'Bemowo', 'Białołęka', 'Bielany', 'Mokotów', 'Ochota', 'Praga-Południe', 'Praga-Północ', 'Rembertów',
    'Śródmieście', 'Targówek', 'Ursus', 'Ursynów', 'Wawer', 'Wesoła', 'Wilanów', 'Włochy', 'Wola', 'Żoliborz',
    'Marki', 'Wołomin', 'Zielonka', 'Ząbki', 'Łomianki', 'Piaseczno', 'Pruszków', 'Grodzisk', 'Legionowo', 
    'Nadarzyn', 'Konstancin-Jeziorna' ,'Piastów', 'Józefów', 'Nowy Dwór', 'Jabłonna', 'Stare Babice'
]

def change_location(location):
    for district in districts:
        if district.lower() in location.lower():
            return district
    return location

df['Location'] = df['Location'].apply(change_location)
```
To standardize the location information in the 'Location' column by replacing specific location names with their corresponding districts if a match is found. 

```python
df['Index'] = range(1, len(df) + 1)
df.set_index('Index', inplace=True)
```
Is used to reassign index values and set a new column as the DataFrame index.

```python
top10 = df['Location'].value_counts().head(10)

plt.figure(figsize=(10, 6))
ax = top10.plot(kind='bar', title='Top 10 Locations by Listings Count')

for i, count in enumerate(top10):
    ax.text(i, count, str(count), ha='center', va='bottom', fontsize=10)

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
```
<p align="center">
  <img src="https://github.com/rusinmt/portfolio/assets/143091357/66c70f48-8cee-4cf0-baa4-000b0bc3cf8a">
</p>

The code calculates the count of Apartment listings by Location, sets a specific size for a Matplotlib figure, displays a text label for each location with text alignment options, and rotates x-axis labels. This visual representation helps identify the most popular areas based on listing counts.
```python
top_location = df.groupby('Location')['Price'].agg(['mean']).sort_values(by='mean', ascending=False).head(30)

top_location.index.name = 'Location'

top_location.sort_values(by='mean', ascending=False, inplace=True)

top_location.plot(kind='bar', 
                  title='Locations by Mean Price', 
                  xlabel='Location', 
                  ylabel='Mean Price'
                 )

plt.xticks(rotation=90)

plt.show()
```

<p align="center">
  <img src="https://github.com/rusinmt/portfolio/assets/143091357/c8da2a50-a1e5-4f9b-8c45-1bdb895dbabb" width="600">
</p>

This code calculates the mean price of apartments in each location by grouping the data by the 'Location' column and then aggregating the 'Price' column using the mean function. The results are sorted in descending order by mean price.

<p align="center">
  <img src="https://github.com/rusinmt/portfolio/assets/143091357/2cc5556c-bee7-4b6f-9c9b-73104987320a" alt="m_sqmup" width="600">
</p>

Same method is used for creating a bar chart for SQMUP by mean price.
```python
otodata = df.to_dict(orient='records')
file_path = 'desktop/otodom_data.json'
with open(file_path, 'w') as json_file:
    json.dump(otodata, json_file, indent=4)
```
To convert each row of the DataFrame into a dictionary, store them as a list, and then write the data into an open JSON file, specifying the path where it will be saved.

## Setting up Azure Data Factory and Snowflake connection

Creating a new Resource group for a Storage Account and establishing Blob Storage within it to upload the otodom_data.json file to a container. Within a Data Factory, setting up linked service connections for Azure Blob Storage data source and Snowflake Warehouse destination table.

<p align="center">
    <img src="https://github.com/rusinmt/portfolio/assets/143091357/e9b79119-384c-4110-87e3-544f851b7590">
</p>

To ensure that the data is loaded correctly in the Copy Data activity, schema mapping defines how columns in the source dataset correspond to fields in the destination dataset.

<p align="center">
    <img src="https://github.com/rusinmt/portfolio/assets/143091357/f37d9d38-5d99-4fb8-a62f-5410ca0924ce" width="700">
</p>

Setting up Snowflake structure.

```sql
create warehouse OTODOM_WH
use warehouse OTODOM_WH

create file format json_format
    type = JSON
```
Creating a warehouse to allocate resources for data processing. Specifying a file format for loading data.
```sql
create or replace TABLE OTODOM_DATA (
	LISTING VARCHAR(16777216),
	PRICE NUMBER(38,0),
	SQMUP NUMBER(38,0),
	ROOM_INFO NUMBER(38,0),
	AREA NUMBER(38,0),
	LOCATION VARCHAR(16777216),
	ADS VARCHAR(16777216)
)
```
Defining schema for a Snowflake table.
```sql
delete from PROJECT.DATA.OTODOM_DATA
where LOCATION not in (
    'Bemowo', 'Białołęka', 'Bielany', 'Mokotów', 'Ochota', 'Praga-Południe',
    'Praga-Północ', 'Rembertów', 'Śródmieście', 'Targówek', 'Ursus', 'Ursynów',
    'Wawer', 'Wesoła', 'Wilanów', 'Włochy', 'Wola', 'Żoliborz'
)

select * from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Targówek'
order by PRICE desc

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Targówek'
    and PRICE > 55000000
```
Using this SQL query to remove locations other than the eighteen Warsaw Districts and eliminate other outliers missed previously.

## Tableau Dashboard

<p align="center">
    <img src="https://github.com/rusinmt/portfolio/assets/143091357/fb9e78b7-a1fb-4145-985c-ae5224e249a3" width="250">
</p>

Loading the transformed data into Tableau via a connection to a Snowflake server.

<p align="center">
    <img src="https://github.com/rusinmt/portfolio/assets/143091357/5d564bad-cf1a-47a8-88f1-e8a72cde74a4" width="500">
</p>

For the Fill Map visualisation of Warsaw district borders, the [GIS Support](https://gis-support.pl/baza-wiedzy-2/dane-do-pobrania/granice-administracyjne/) site aids the effort of providing [Geometry Measurers](https://gis-support.pl/wp-content/uploads/dzielnice_Warszawy.zip) in a Spatial file format.

The dashboard offers key insights into apartment listings on otodom.pl in Warsaw, providing a range of essential indicators. It includes information on both the highest and lowest property prices, along with area and square meter prices, offering a comprehensive view of the market's pricing dynamics, showcasing extreme values.
Interactive map highlighting districts average property parameters, including price, area, and square meter price. Furthermore, the dashboard categorizes the types of advertisements found on the otodom.pl webpage, aiding users in understanding the market landscape. Moreover, the dashboard highlights the top five districts with the highest number of listings. Users can interact with a map equipped with slider filters, allowing for dynamic exploration and analysis of these districts.

<p align="center">
    <img src="https://github.com/rusinmt/portfolio/assets/143091357/9829fc04-f26a-4e80-8103-1054a2d63e08" width="550">
</p>

The Price Percentile of listings help us understand the distribution of apartments for sale in the dataset. The 10th percentile illustrates the lower end of the price range, highlighting cheaper apartments and bargains. The median maintains the overall pricing tendencies in the dataset. Separating the data at the 90th percentile excludes 90% of apartments for sale, leaving us with the most expensive offers.

<p align="center">
    <img src="https://github.com/rusinmt/portfolio/assets/143091357/849288ea-32b7-43f6-a964-4470095c2b9b" width="600">
</p>

To add a Compact list of calcalated parameters to the visual,

```tableau
IF [Map Metric] = 'Average Price'
THEN AVG([PRICE])

ELSEIF [Map Metric] = 'Average Area'
THEN AVG([AREA])

ELSEIF [Map Metric] = 'Average SQMUP'
THEN AVG([SQMUP])

END
```
 a calculated field was established.

The Price Percentile and Top 5 Districts by Listing count graph are independent from the drill down action when a specfic district is selected. thanks to the implementation of Filter Actions. Additionally, highlighting has been disabled to ensure a more intuitive user experience

<p align="center">
    <img src="https://github.com/rusinmt/portfolio/assets/143091357/6546c882-3dd2-4599-b0e7-92642add0e4f" width="250">
</p>

Method involves using a random string value in a Calculated field 'NO Higlight' placing in the Detail shelf and selecting in the Higlighter.

In essence, the dashboard serves as a tool for gaining insights into Warsaw's real estate market as reflected in advertisements on otodom.pl, offering a wide range of data and visualizations to support informed expansion of the agency's portfolio.
