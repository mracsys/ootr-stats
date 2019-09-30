/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [ootstat].[item], [ootstat].[ootpct], [kakstat].[kakpct] FROM
  (SELECT [item], COUNT([item]) * 100.0 / 10000.0 AS [ootpct]
  FROM [OotrStatsDF].[dbo].[items]
  WHERE [loc] = 'Song from Ocarina of Time' AND [item] = 'Zeldas Lullaby'
  GROUP BY [item]) AS [ootstat] LEFT OUTER JOIN
  (SELECT [item], COUNT([item]) * 100.0 / 10000.0 AS [kakpct]
  FROM [OotrStatsDF].[dbo].[items]
  WHERE [loc] = 'Sheik in Kakariko' AND [item] = 'Zeldas Lullaby'
  GROUP BY [item]) AS [kakstat] ON [ootstat].[item] = [kakstat].[item]