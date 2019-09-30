/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [item], COUNT([item]) * 100.0 / 10000.0 AS [ootpct]
  FROM [OotrStatsDF].[dbo].[items]
  WHERE [loc] = 'Song from Ocarina of Time'
  GROUP BY [item]
  ORDER BY [ootpct] DESC