import sqlite3
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

data_min_size = 4800

conn = sqlite3.connect('./training.db')
c = conn.cursor()

# clear training data
c.execute('delete from training_set')

# get eligible styles
c.execute('select s.ID from recipes r join styles s on s.ID = r.styleID \
group by styleID having count(r.styleID) >= (?)', (data_min_size,))
style_ids = c.fetchall()

# insert min data from each style
for style_id in style_ids:
    c.execute('insert into training_set (recipeID, styleID) \
        select id as recipeID, styleID from recipes \
        where styleID = (?) order by random() limit (?)', (style_id[0], data_min_size))

print("styles: " + str(len(style_ids)))
print("rows per: " + str(data_min_size))
print("total: " + str(data_min_size*len(style_ids)))

conn.commit()
c.close()
conn.close()
