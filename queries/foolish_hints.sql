SELECT loc, COUNT(seed) * 100.0 / 100000 as foolish_hint_num
FROM (SELECT DISTINCT loc, seed
  FROM hints
  WHERE htype = 'fool') AS foolhints
  GROUP BY loc
  ORDER BY loc ASC
