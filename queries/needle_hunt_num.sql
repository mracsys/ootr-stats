SELECT DISTINCT obvious_items.seed
FROM obvious_items LEFT JOIN
(SELECT seed,MAX(sphere) AS topsphere
FROM obvious_items
GROUP BY seed) AS [totspheres] ON (totspheres.seed = obvious_items.seed AND totspheres.topsphere = obvious_items.sphere)
WHERE (NOT totspheres.topsphere IS NULL) AND obvious_items.obvious = 'No'