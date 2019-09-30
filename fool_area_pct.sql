/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [area]
      ,[pct]
  FROM [OotrStatsDF].[dbo].[fool_area] ORDER BY [pct] DESC