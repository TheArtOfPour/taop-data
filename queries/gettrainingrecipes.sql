select count(yeastID), y.name
from recipe_yeast ry
join yeast y on y.id = ry.yeastID
group by yeastID
--having count(yeastID) < 90
order by count(yeastID) desc