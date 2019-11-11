/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [item], COUNT([item]) * 100.0 / 100000.0 AS [adpct]
  FROM [OotrStatsS3].[dbo].[spheres]
  WHERE [loc] = 'Song from Ocarina of Time'
  GROUP BY [item]
  ORDER BY [adpct] DESC