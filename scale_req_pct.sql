/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [scale_req]
      ,[pct]
  FROM [OotrStatsS3].[dbo].[scale_reqs] ORDER BY [scale_req] ASC