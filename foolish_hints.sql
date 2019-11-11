/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [loc], COUNT([seed]) * 100.0 / 100000 as [foolish_hint_num]
FROM (SELECT DISTINCT [loc], [seed]
  FROM [OotrStatsS3].[dbo].[hints]
  WHERE [htype] = 'fool') AS [foolhints]
  GROUP BY [loc]
  ORDER BY [loc] ASC
