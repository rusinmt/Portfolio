SELECT 
  [DateKey], 
  [FullDateAlternateKey] AS Date, 
  [EnglishDayNameOfWeek] AS Day,
  [WeekNumberOfYear] AS WeekNr, 
  [EnglishMonthName] AS Month,
  LEFT([EnglishMonthName],3) AS MonthShort,
  [MonthNumberOfYear] AS MonthNo, 
  [CalendarQuarter] AS Quarter, 
  [CalendarYear] As Year
FROM 
  [AdventureWorksDW2022].[dbo].[DimDate]
  WHERE CalendarYear >=2019
  AND
    CalendarYear < 2023 OR (CalendarYear = 2023 AND MonthNumberOfYear <= 1)