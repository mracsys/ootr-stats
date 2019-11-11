/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [hook_req]
      ,[pct]
  FROM [OotrStatsS3].[dbo].[hook_reqs] ORDER BY [hook_req] ASC