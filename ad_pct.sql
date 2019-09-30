/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [item], COUNT([item]) * 100.0 / 10000.0 AS [adpct]
  FROM [OotrStatsDF].[dbo].[spheres]
  WHERE [loc] = 'Song from Ocarina of Time'
  GROUP BY [item]
  ORDER BY [adpct] DESC