import sqlite3
import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from db import RecipeDB

data_min_size = 5000
style_min = 6775
yeast_min = 1500
hops_min = 3500
fermentables_min = 3000

rconn = sqlite3.connect('./recipes.db')
rc = rconn.cursor()
qry = open('cleardb.sql', 'r').read()
tconn = sqlite3.connect('./training.db')
tc = tconn.cursor()
tc.executescript(qry)

rc_recipe_db = RecipeDB()
tc_recipe_db = RecipeDB(tconn)

# fetch candidates from recipe db
rc.execute('select styleID from recipes group by styleID having count(styleID) >= (?)', (style_min,))
style_ids = rc.fetchall()
print(len(style_ids), " styles")
rc.execute('select yeastID from recipe_yeast group by yeastID having count(yeastID) >= (?)', (yeast_min,))
yeast_ids = rc.fetchall()
print(len(yeast_ids), " yeast")
rc.execute('select hopID from recipe_hops group by hopID having count(hopID) >= (?)', (hops_min,))
hop_ids = rc.fetchall()
print(len(hop_ids), " hops")
rc.execute('select fermentableID from recipe_fermentables group by fermentableID having count(fermentableID) >= (?)',
           (fermentables_min,))
fermentable_ids = rc.fetchall()
print(len(fermentable_ids), " fermentables")

print("Fetching recipes")
# Filter one to one
params = []
for style_id in style_ids:
    params.append(style_id[0])
for yeast_id in yeast_ids:
    params.append(yeast_id[0])
rc.execute(
    'select distinct id from recipes r '
    'join recipe_yeast ry on r.id = ry.recipeID '
    'join recipe_hops rh on r.id = rh.recipeID '
    'join recipe_fermentables rf on r.id = rf.recipeID '
    'where r.styleID in ({styles}) '
    'and ry.yeastID in ({yeast})'.format(
        styles=','.join(['?'] * len(style_ids)),
        yeast=','.join(['?'] * len(yeast_ids)),
    ),
    params)
recipe_ids = rc.fetchall()

print("Pruning recipes")
# Filter one to many
pruned_recipe_ids = []
for recipe_id in recipe_ids:
    params = [recipe_id[0]]
    for fermentable_id in fermentable_ids:
        params.append(fermentable_id[0])
    rc.execute(
        'SELECT count(rf.fermentableID) FROM recipe_fermentables rf '
        'WHERE rf.recipeID=? AND rf.fermentableID NOT IN ({fermentables})'.format(
            fermentables=','.join(['?'] * len(fermentable_ids)),
        ),
        params)
    prune_fermentables = rc.fetchone()
    if prune_fermentables[0] > 0:
        continue

    params = [recipe_id[0]]
    for hop_id in hop_ids:
        params.append(hop_id[0])
    rc.execute(
        'SELECT count(rh.hopID) FROM recipe_hops rh '
        'WHERE rh.recipeID=? AND rh.hopID NOT IN ({hops})'.format(
            hops=','.join(['?'] * len(hop_ids)),
        ),
        params)
    prune_hops = rc.fetchone()
    if prune_hops[0] > 0:
        continue
    pruned_recipe_ids.append(recipe_id[0])

# insert into training db
total = len(pruned_recipe_ids)
tenth = int(total / 10)
count = 0
print("Recipes: " + str(total))
print("Inserting [", end="")
for recipe_id in pruned_recipe_ids:
    if count % tenth == 0:
        print("-", end="")
    recipe_model = rc_recipe_db.get_recipe(int(recipe_id))
    tc_recipe_db.insert_recipe(recipe_model)
    count += 1
print("] complete!")

# clear training data
tc.execute('delete from training_set')

# get eligible styles
tc.execute('select s.ID from recipes r join styles s on s.ID = r.styleID \
group by styleID having count(r.styleID) >= (?)', (data_min_size,))
style_ids = tc.fetchall()

# insert min data from each style
for style_id in style_ids:
    tc.execute('insert into training_set (recipeID, styleID) \
        select id as recipeID, styleID from recipes \
        where styleID = (?) order by random() limit (?)', (style_id[0], data_min_size))

print("styles: " + str(len(style_ids)))
print("rows per: " + str(data_min_size))
print("total: " + str(data_min_size * len(style_ids)))

rconn.commit()
rc.close()
rconn.close()

tconn.commit()
tc.close()
tconn.close()
