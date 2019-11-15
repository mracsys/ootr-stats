SELECT item, COUNT(item) * 100.0 / 100000.0 AS ootpct
  FROM items
  WHERE loc = 'Song from Ocarina of Time'
  GROUP BY item
  ORDER BY ootpct DESC