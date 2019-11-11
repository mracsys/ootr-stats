/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [loc], COUNT([seed]) * 100.0 / 100000.0 AS [unhinted]
  FROM [OotrStatsS3].[dbo].[non_hinted_loc]
  GROUP BY [loc]
  ORDER BY [unhinted] DESC