--select * from styles -- saison 15
select avg(og) as og, avg(fg) as fg, avg(srm) as srm, avg(ibu) as ibu from recipes where styleID = 15