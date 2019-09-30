/****** Script for SelectTopNRows command from SSMS  ******/
SELECT DISTINCT [loc], COUNT([seed]) * 100.0 / 10000.0 AS [unhinted]
  FROM [OotrStatsDF].[dbo].[non_hinted_loc]
  WHERE [norm_sphere] >= 60
  GROUP BY [loc]
  ORDER BY [unhinted] DESC