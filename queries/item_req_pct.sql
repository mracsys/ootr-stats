SELECT item, COUNT(seed) * 100.0 / 100000 AS required
FROM spheres
GROUP BY item
ORDER BY item