select r.name as recipe, s.name as style, y.name as yeast, f.*, h.*
from recipes r
join styles s on r.styleID = s.ID
join recipe_fermentables rf on rf.recipeID = r.ID
join fermentables f on rf.fermentableID = f.ID
join recipe_hops rh on rh.recipeID = r.ID
join hops h on rh.hopID = h.ID
join recipe_yeast ry on ry.recipeID = r.ID
join yeast y on ry.yeastID = y.ID
where r.ID = 49107;