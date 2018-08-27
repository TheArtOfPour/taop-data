select h.id, h.name, count(rh.recipeID) as ct
from recipe_hops rh
join hops h on rh.hopID = h.id
join recipes r on rh.recipeID = r.id
join recipe_fermentables rf on r.id = rf.recipeID
join fermentables f on rf.fermentableID = f.id
where r.styleID = 4 -- american ipa
and f.id = 27 -- golden promise
group by rh.hopID
--having count(styleID) > 2000
order by ct desc;


-- american ipa - MO, Golden Promise or Wheat or Oats : citra/mosaic
-- 2 row : cascades
-- rye : amarillo much more common