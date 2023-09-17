SELECT 
  p.[ProductKey], 
  p.[ProductAlternateKey] AS ProductItemCode, 
  p.[EnglishProductName] AS ProductName, 
  ps.EnglishProductSubcategoryName AS SubCategory, 
  pc.EnglishProductCategoryName AS PruductCategory,
  p.[StandardCost],
  p.[Color] AS ProductColor, 
  p.[Size] AS ProductSize, 
  p.[ProductLine], 
  p.[ModelName] AS ProductModelName, 
  p.[EnglishDescription] AS PruductDescription,
  ISNULL (p.Status, 'Outdated') AS ProductStatus 
FROM 
  [dbo].[DimProduct] AS p 
  LEFT JOIN dbo.DimProductSubcategory AS ps ON ps.ProductSubcategoryKey = p.ProductSubcategoryKey 
  LEFT JOIN dbo.DimProductCategory AS pc ON ps.ProductCategoryKey = pc.ProductCategoryKey 
order by 
  p.ProductKey ASC