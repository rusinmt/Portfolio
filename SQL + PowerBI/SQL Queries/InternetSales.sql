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
