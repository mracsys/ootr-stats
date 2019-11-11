SELECT [loc], [hint_type], COUNT([seed]) * 100.0 / 100000
FROM [woth_types]
GROUP BY [loc], [hint_type]
ORDER BY [loc] ASC