/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [area]
      ,[pct]
  FROM [OotrStatsS3].[dbo].[fool_area] ORDER BY [pct] DESC