select f.id, f.name, count(ry.recipeID) as ct
from recipe_yeast ry
join yeast f on ry.yeastID = f.id
join recipes r on ry.recipeID = r.id
where r.styleID = 15
group by ry.yeastID
--having count(styleID) > 2000
order by ct desc;