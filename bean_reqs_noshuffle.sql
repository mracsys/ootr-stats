/****** Script for SelectTopNRows command from SSMS  ******/
SELECT [fsphere].[loc], COUNT([fsphere].[loc])
  FROM [OotrStatsS3].[dbo].[ispheres] as [csphere]
  LEFT JOIN [OotrStatsS3].[dbo].[ispheres] as [fsphere] ON ([csphere].[seed] = [fsphere].[seed] AND [csphere].[item] = 'Magic Bean' AND 
  ([fsphere].[loc] = 'Colossus Freestanding PoH' OR
  [fsphere].[loc] = 'Graveyard Freestanding PoH' OR
  [fsphere].[loc] = 'DM Crater Volcano Freestanding PoH' OR
  [fsphere].[loc] = 'Lake Hylia Freestanding PoH' OR
  [fsphere].[loc] = 'Adult Fishing'))
  WHERE NOT [fsphere].[seed] IS NULL AND [fsphere].[sphere] > [csphere].[sphere]
  GROUP BY [fsphere].[loc]