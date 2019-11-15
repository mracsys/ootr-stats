SELECT DISTINCT area, COUNT(seed) * 100.0 / 100000.0 AS unhinted
  FROM non_hinted_loc
  GROUP BY area
  ORDER BY unhinted DESC