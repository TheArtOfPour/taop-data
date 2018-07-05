select f.id, f.name, count(rf.recipeID) as ct
from recipe_fermentables rf
join fermentables f on rf.fermentableID = f.id
join recipes r on rf.recipeID = r.id
where r.styleID = 15
group by rf.fermentableID
--having count(styleID) > 2000
order by ct desc;