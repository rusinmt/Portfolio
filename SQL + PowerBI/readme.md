## Sales Report for Adventure Works Cycles

In the realm of business, much like in life itself, our decision-making processes often requires us to navigate through uncertain future, shrouded in ambiguity. Predictions and long-term strategic plans frequently necessitate adaptation to the ever-evolving and dynamic environment. 
Adventure Works Cycles, for past three years, encounters formidable challenges in the global market, primarily centered around the strategic allocation of resources to optimize profitability and the imperative to render budget planning more flexible, capable of responding to external events that exert influence on the economy.

###Project Objective:
The primary objective of this initiative is to provide Adventure Works Cycles with strategic guidance to identify the most profitable markets and augment the flexibility of their budget planning processes.

Setting up a data model in Power BI using a well-known star schema begins with defining the Fact Table from the restored and updated AdventureWorksDW2022 database in MS SQL Server.
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
In witch I defined specific period in the scope of analysis using the OrderDateKey from last 3 tears.
