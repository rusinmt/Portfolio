SELECT
    d.SalesTerritoryKey,
	d.SalesTerritoryRegion,
    d.SalesTerritoryCountry,
    SUM(f.SalesAmount) AS [Sales]
FROM DimSalesTerritory d
JOIN FactInternetSales f ON d.SalesTerritoryKey = f.SalesTerritoryKey
GROUP BY d.SalesTerritoryCountry, d.SalesTerritoryRegion, d.SalesTerritoryKey
ORDER BY [Sales] DESC;