/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [area]
      ,[pct]
  FROM [OotrStatsS3].[dbo].[woth_item_area] ORDER BY [pct] DESC