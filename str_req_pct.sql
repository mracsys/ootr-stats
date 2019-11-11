/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [str_req]
      ,[pct]
  FROM [OotrStatsS3].[dbo].[str_reqs] ORDER BY [str_req] ASC