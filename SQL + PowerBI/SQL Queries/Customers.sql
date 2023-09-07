SELECT 
  c.customerkey AS CustomerKey, 
  c.firstname AS FirstName, 
  c.lastname AS LastName, 
  c.firstname + ' ' + lastname As FullName,
  CASE c.gender WHEN 'M' THEN 'Male' WHEN 'F' Then 'Female' END AS Gender,
  c.datefirstpurchase AS DateFirstPurchase,
  g.city AS CustomerCity
FROM 
  dbo.dimcustomer AS c 
  LEFT JOIN dbo.dimgeography AS g ON g.geographykey = c.geographykey 
ORDER BY 
  CustomerKey ASC
