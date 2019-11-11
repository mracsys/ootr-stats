/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [seed]
      ,[max_sphere]
  FROM [OotrStatsS3].[dbo].[total_spheres] ORDER BY [seed]