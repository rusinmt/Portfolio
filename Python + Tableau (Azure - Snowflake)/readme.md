## Exploring Apartment Advertisements in Warsaw

Just as a farmer carefully selects the most fertile land for planting crops, real estate professionals must identify the most promising locations for property investments. 
As in agriculture, where the growth of crops necessitates diligent care and timely harvests, the growth of a real estate portfolio demands a proactive approach, seizing opportunities and nurturing investments for continued success.

This project addresses this challenge by leveraging data extraction methods to support the real estate market needs and provide insights into the most suitable locations for agencies to expand their portfolios. Through data-driven visuals, this endeavor strives to provide real estate agencies with valuable insights and recommendations regarding optimal locations for portfolio expansion within the city limits of Warsaw.

## Process Archtecture

![gif](https://github.com/rusinmt/portfolio/assets/143091357/aaff7b14-2479-43d8-8d0c-377eb57629a6)

Python takes the lead in extracting comprehensive information on flats available for sale in Warsaw, covering vital factors like price, area, room count, and price per square meter. Through exploratory data analysis provides deeper understanding of the dataset. Upon initial contact with the data, it is thoughtfully exported to a JSON file format. 
An Azure Blob Storage Container is established within the Azure Data Factory to house the dataset, followed by a seamless transition of data into the Snowflake Warehouse. 
SQL queries are then applied to prepare the data for advanced analysis. Tableau brings the insights to life, enabling the creation of dynamic dashboards. Geospatial analysis provides a district-level perspective on property locations, price trends, room distribution, and price per square meter insights. Armed with these findings, real estate professionals can make informed decisions.
