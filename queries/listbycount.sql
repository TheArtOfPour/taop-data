select s.name, count(r.styleID) as ct
from styles s
join recipes r on r.styleID = s.id
group by styleID
having count(styleID) > 7000
order by ct desc;