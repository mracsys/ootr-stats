SELECT DISTINCT items.item, COUNT(items.seed) / 10.0 as item_pct
FROM items
LEFT JOIN locations on items.loc = locations.loc
LEFT JOIN unique_items ON unique_items.item = items.item
WHERE locations.area = 'Deku Tree' AND unique_items.itype = 'Required' AND items.item != 'Kokiri Sword'
GROUP BY items.item
ORDER BY item_pct DESC