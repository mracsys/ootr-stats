/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [loc]
      ,[pct]
  FROM [OotrStatsS3].[dbo].[woth_loc] ORDER BY [pct] DESC