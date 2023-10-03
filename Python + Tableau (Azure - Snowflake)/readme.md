## Exploring Apartment Advertisements in Warsaw

Just as a farmer carefully selects the most fertile land for planting crops, real estate professionals must identify the most promising locations for property investments. 
As in agriculture, where the growth of crops necessitates diligent care and timely harvests, the growth of a real estate portfolio demands a proactive approach, seizing opportunities and nurturing investments for continued success.

This project addresses this challenge by leveraging data extraction methods to support the real estate market needs and provide insights into the most suitable locations for agencies to expand their portfolios. Through data-driven visuals, this endeavor strives to provide real estate agencies with valuable insights and recommendations regarding optimal locations for portfolio expansion within the city limits of Warsaw.

## Process Archtecture

![gif](https://github.com/rusinmt/portfolio/assets/143091357/aaff7b14-2479-43d8-8d0c-377eb57629a6)

Python takes the lead in extracting comprehensive information about flats available for sale in Warsaw, focusing on critical factors like price, area, room count, and price per square meter. Through exploratory data analysis, it delves deeper into the dataset, enhancing our understanding. Upon initial contact with the data, it's thoughtfully exported to a JSON file format. An Azure Blob Storage Container is established in the Azure cloud environment to house the dataset, and then it seamlessly transitions with Azure Data Factory, creating a connection into the Snowflake Warehouse. SQL queries are skillfully applied to prepare the data for advanced analysis. Tableau steps in to bring the insights to life, allowing for the creation of dynamic dashboards. Geospatial analysis provides a district-level perspective on property locations, price trends, room distribution, and price per square meter insights. Equipped with these findings, real estate professionals can make informed decisions to navigate the market effectively.
