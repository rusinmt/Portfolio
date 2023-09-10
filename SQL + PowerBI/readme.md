## Sales Report for Adventure Works Cycles

In the realm of business, much like in life itself, our decision-making processes often requires us to navigate through uncertain future, shrouded in ambiguity. Predictions and long-term strategic plans frequently necessitate adaptation to the ever-evolving and dynamic environment. 
Adventure Works Cycles, for past three years, encounters formidable challenges in the global market, primarily centered around the strategic allocation of resources to optimize profitability and the imperative to render budget planning more flexible, capable of responding to external events that exert influence on the economy.

### Project Objective:
The primary objective of this initiative is to provide Adventure Works Cycles with strategic guidance to identify the most profitable markets and augment the flexibility of their budget planning processes.

### Data Wrangling:
Setting up a data model in Power BI using a well-known star schema begins with defining the fact table FACT_InternetSales from the restored and updated ([AdventureWorksDW2022](https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorksDW2022.bak)) database in MS SQL Server.
```sql
SELECT 
  [ProductKey], 
  [OrderDateKey], 
  [DueDateKey], 
  [ShipDateKey], 
  [CustomerKey],
  [SalesTerritoryKey],
  [SalesOrderNumber],
  [OrderQuantity],
  [ProductStandardCost],
  [SalesAmount]
FROM 
  [dbo].[FactInternetSales]
WHERE 
  LEFT([OrderDateKey], 4) >= YEAR(GETDATE()) - 3 
ORDER BY 
  OrderDateKey ASC;
```
In which I defined specific period in the scope of analysis using the OrderDateKey from last 3 tears.
Filtered dimension table DIM_Calendar uses newly created, renamed columns,
```sql
 LEFT([EnglishMonthName],3) AS MonthShort,
```
and data from 2020 until the first month of 2023.
```sql
  WHERE CalendarYear >=2020
  AND
    CalendarYear < 2023 OR (CalendarYear = 2023 AND MonthNumberOfYear <= 1)
```

```sql
  c.firstname + ' ' + lastname As FullName,
  CASE c.gender WHEN 'M' THEN 'Male' WHEN 'F' Then 'Female' END AS Gender,
  c.datefirstpurchase AS DateFirstPurchase,
  g.city AS CustomerCity
FROM 
  dbo.dimcustomer AS c 
  LEFT JOIN dbo.dimgeography AS g ON g.geographykey = c.geographykey 
ORDER BY 
  CustomerKey ASC
```
Customers table concatenates FirstName column with LastName and assings it an alias 'FullName'. Creates a new column with gender information, checking the values and assinging them 'Male' if the value stated is 'M' and 'Female' for 'F'. Finnaly LEFT JOIN based on GeographyKey, dbo.dimgeography joins records with dbo.customer table adding g.city column with assigned alias 'CustomerCity'.
```sql
   SUM(f.SalesAmount) AS [Sales]
FROM DimSalesTerritory d
JOIN FactInternetSales f ON d.SalesTerritoryKey = f.SalesTerritoryKey
GROUP BY d.SalesTerritoryCountry, d.SalesTerritoryRegion, d.SalesTerritoryKey
ORDER BY [Sales] DESC
```
The DIM_SalesTerritory table groups the sum of SalesAmount for each sales territory and orders the results by three specified columns in descending order.
```sql
ISNULL (p.Status, 'Outdated') AS ProductStatus 
FROM 
  [dbo].[DimProduct] AS p 
  LEFT JOIN dbo.DimProductSubcategory AS ps ON ps.ProductSubcategoryKey = p.ProductSubcategoryKey 
  LEFT JOIN dbo.DimProductCategory AS pc ON ps.ProductCategoryKey = pc.ProductCategoryKey 
```
The ISNULL function checks the 'Status' column in the DimProduct table. If the column has no value, it assigns the default value 'Outdated' to the 'ProductStatus' column. However, if there is information in the 'Status' column, it returns that information. Additionally, the query uses LEFT JOIN operations to add subcategory and category records to the DimProduct table from related tables.

### Power BI Modeling

Exported CSV files are imported to Power BI. Primary Keys, identifying the tables, will now be used to define relationships and create a data model.
![model](https://github.com/rusinmt/portfolio/assets/143091357/14987950-1e98-4daf-9404-ee5a7511306d)
