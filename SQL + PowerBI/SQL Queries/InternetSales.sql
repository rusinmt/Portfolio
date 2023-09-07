SELECT 
  [ProductKey], 
  [OrderDateKey], 
  [DueDateKey], 
  [ShipDateKey], 
  [CustomerKey],  
  [SalesOrderNumber],
  [SalesAmount]
FROM 
  [dbo].[FactInternetSales] 
WHERE 
  LEFT (OrderDateKey, 4) >= YEAR(GETDATE()) -4
ORDER BY 
  OrderDateKey ASC