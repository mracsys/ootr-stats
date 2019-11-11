/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [40stat].[item], [40stat].[40pct], [50stat].[50pct] FROM
  (SELECT [item], COUNT([item]) * 100.0 / 100000.0 AS [40pct]
  FROM [OotrStatsS3].[dbo].[items]
  WHERE [loc] = '40 Gold Skulltula Reward'
  GROUP BY [item]) AS [40stat] LEFT OUTER JOIN
  (SELECT [item], COUNT([item]) * 100.0 / 100000.0 AS [50pct]
  FROM [OotrStatsS3].[dbo].[items]
  WHERE [loc] = '50 Gold Skulltula Reward'
  GROUP BY [item]) AS [50stat] ON [40stat].[item] = [50stat].[item] ORDER BY [40stat].[item]