/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [area]
      ,[pct]
  FROM [OotrStatsDF].[dbo].[woth_area] ORDER BY [pct] DESC