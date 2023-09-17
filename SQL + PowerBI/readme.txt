## Sales Report for Adventure Works Cycles

In the realm of business, much like in life itself, our decision-making processes often requires us to navigate through uncertain future, shrouded in ambiguity. Predictions and long-term strategic plans frequently necessitate adaptation to the ever-evolving and dynamic environment. 
Adventure Works Cycles, for past three years, encounters formidable challenges in the global market, primarily centered around the strategic allocation of resources to optimize profitability and the imperative to render budget planning more flexible, capable of responding to external events that exert influence on the economy.

### Project Objective:
The primary objective of this initiative is to provide Adventure Works Cycles with strategic guidance to identify the most profitable markets and augment the flexibility of their budget planning processes.

### Data Wrangling:
Setting up a data model in Power BI using a well-known star schema begins with defining the fact table FACT_InternetSales from the restored and updated [AdventureWorksDW2022](https://github.com/Microsoft/sql-server-samples/releases/download/adventureworks/AdventureWorksDW2022.bak) database in MS SQL Server.
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

Providing random Budget values in DIM_Budget for training purposes.

### Power BI Modeling:

Exported CSV files are imported to Power BI. Primary Keys, identifying the tables, will now be used to define relationships and create a data model.

<p align="center">
  <img src="https://github.com/rusinmt/portfolio/assets/143091357/14987950-1e98-4daf-9404-ee5a7511306d)">
</p>
    
Defining Key Measures in DAX, for analyzing and visualizing data within given time period.
```dax
Sales = SUM ( FACT_InternetSales[SalesAmount] )
```
Total Sales as 'Sales'
```dax
Budget Amount = SUM ( FACTS_Budget[Budget] )
```
'Budget Amount" sum of Budget column, and 'Sales / Budget' for dynamic KPI visualisation to show sales and budget variance during significant budget expenditure.
```dax
Sales / Budget = [Sales] - [Budget Amount]
Cost = SUM(FACT_InternetSales[ProductStandardCost] )
Profit Margin = [Sales] - [Cost] 
Profit Margin % = DIVIDE( [Profit Margin], [Sales], 0 )
```
Usage of the third argument in 'Profit Margin %' will eansure that if the denominator is 0, formula will return '0' instead of producing an error.

### Dashboard:

<p align="center">
  <img src="https://github.com/rusinmt/portfolio/assets/143091357/aaaabade-d14d-4cb7-a916-04144389cdb3" width="250" >
</p>
    
In the charts, there's a highlighting mechanism connected to the month slicer through an additional hidden synchronized slicer. This hidden slicer draws its values from a separate table that is not directly linked to the main data model. The functionality is achieved using the following DAX code.
```dax
SalesChartUnpluged = 
CALCULATE(
    [Sales],
    TREATAS(VALUES(DIM_ChartUnpluged[MonthShort]), DIM_Calendar[MonthShort])
    )
```
This measure establishes a virtual relationship between the DIM_Calendar table in the model, and its DIM_ChartUnplugged counterpart outside. This connection is based on the common 'MonthShort' column. It enables calculations as though the two tables were related by month, even in cases where there is no direct relationship between them in the data model.
HIghlight Sales = 
```dax
IF(
    SELECTEDVALUE('DIM_Calendar'[MonthShort]) = SELECTEDVALUE('DIM_ChartUnpluged'[MonthShort]),
    [SalesChartUnpluged]
    )
```
Formula returns value of 'SalesChartUnpluged' if the months in two slicers match. This mechanism highlights the 'Sales' data based on users the month selection.

In ranking the top 10 Customers by Sales using the 'Top N' filter option, a problem has arisen when multiple clients have the same sales values, resulting in a tie. To address this tiebreak situation.
```dax
Tiebreaker = 
VAR DateFirstPurchase = MIN(DIM_Customers[DateFirstPurchase])
RETURN
[Sales] * DateFirstPurchase * ( RAND() / 10000 )
```
Secondary crieterion of earliest DateFirstPurchase was not sufficient to break the ties among clients. Therfore there is a RAND() function generating  a random decimal number, scaled down by a factor of 10 000.

### Analysis:

The dashboard serves as a comprehensive tool for the Sales Department and managers, offering a detailed overview of sales, client insights, and product details. That could be extended futher to develope the best seeling product or to shift company's focus from equipment and accesories. 
The primary analytics problem revolves around the annual sales performance, which exhibited remarkable growth in 2022, nearly tripling from the previous year, and doubling of profit margins. Markers held up strongly till the end of the year, despite reducing budget spending.

<p align="center">
  <img src="https://github.com/rusinmt/portfolio/assets/143091357/4e1bead1-6cfa-4a52-99a4-def3081b1079" width="550">
</p>

While the percentile profit margin for each country appears almost identical, indicative of efficient regional market management, a distinct gap emerges when analyzing the percentile contribution of each country to the total profit margin. This discrepancy unequivocally highlights the most profitable markets that warrant the company's primary strategic focus.

<p align="center">
  <img src="https://github.com/rusinmt/portfolio/assets/143091357/bb9fe340-5bb1-455a-bee8-22c288586a94" width="300">
</p>

Concerning budgeting and strategy, it is imperative for a company of this magnitude to adopt a long-term vision. This approach ensures a steady trajectory, facilitating dynamic growth and maintaining a position as a formidable competitor.  It is advisable to exercise prudence by integrating safety measures into the strategy, considering potential black swan events that could disrupt the market and impact profitability. Such forward-thinking measures contribute to the maximization of profits and the companys overall resilience.
