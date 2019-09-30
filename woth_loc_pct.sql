/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [loc]
      ,[pct]
  FROM [OotrStatsDF].[dbo].[woth_loc] ORDER BY [pct] DESC