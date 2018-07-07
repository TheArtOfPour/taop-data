import sqlite3

from db.models.fermentable import Fermentable
from db.models.hop import Hop
from db.models.recipe import Recipe


class RecipeDB:
    conn = ''
    c = ''
    styles = {}
    yeast = {}
    hops = {}
    fermentables = {}
    max_hop_count = 11
    max_fermentable_count = 6

    def __init__(self, conn=''):
        if conn != '':
            self.conn = conn
        else:
            self.conn = sqlite3.connect('./recipes.db')

    def close(self):
        self.conn.commit()
        self.conn.close()

    def refresh(self):
        self.conn.commit()
        self.conn.close()
        self.conn = sqlite3.connect('./recipes.db')

    def get_recipe(self, recipe_id):
        c = self.conn.cursor()

        c.execute('SELECT s.name as stylename, y.name as yeastname, og, fg, ibu, srm '
                  'FROM recipes r JOIN styles s ON r.styleID = s.id JOIN recipe_yeast ry ON r.id = ry.recipeID '
                  'JOIN yeast y ON ry.yeastID = y.id WHERE r.id=?',
                  (recipe_id,))
        stylename, yeastname, og, fg, ibu, srm = c.fetchone()
        recipe = Recipe('')
        recipe.og = og
        recipe.fg = fg
        recipe.srm = srm
        recipe.ibu = ibu
        recipe.style = stylename
        recipe.yeast = yeastname
        c.execute('SELECT name, pounds FROM recipe_fermentables rf '
                  'JOIN fermentables f ON rf.fermentableID = f.id WHERE rf.recipeID=?',
                  (recipe_id,))
        fermentables = c.fetchall()
        for name, pounds in fermentables:
            recipe.fermentables.append(Fermentable(name, pounds))
        c.execute('SELECT name, ounces, minutes FROM recipe_hops rh '
                  'JOIN hops h ON rh.hopID = h.id WHERE rh.recipeID=?',
                  (recipe_id,))
        hops = c.fetchall()
        for name, ounces, minutes in hops:
            recipe.hops.append(Hop(name, ounces, minutes))
        return recipe

    def insert_recipe(self, recipe):
        """
        :type recipe: Recipe
        """

        if len(recipe.hops) > self.max_hop_count or len(recipe.fermentables) > self.max_fermentable_count:
            return

        c = self.conn.cursor()

        # style
        if recipe.style not in self.styles:
            c.execute('SELECT id FROM styles WHERE name=(?)', (recipe.style,))
            style_id = c.fetchone()
            if not style_id:
                c.execute('INSERT INTO styles(name) VALUES (?)', (recipe.style,))
                style_id = c.lastrowid
            else:
                style_id = style_id[0]
            self.styles[recipe.style] = style_id
        style_id = self.styles[recipe.style]

        # recipe
        c.execute(
            'INSERT INTO recipes(styleID, og, fg, ibu, srm) VALUES (?, ?, ?, ?, ?, ?)',
            (style_id, recipe.og, recipe.fg, recipe.ibu, recipe.srm,)
        )
        recipe_id = c.lastrowid

        # yeast
        if recipe.yeast == "":
            recipe.yeast = "generic"
        if recipe.yeast not in self.yeast:
            c.execute('SELECT id FROM yeast WHERE name=(?)', (recipe.yeast,))
            yeast_id = c.fetchone()
            if not yeast_id:
                c.execute('INSERT INTO yeast(name) VALUES (?)', (recipe.yeast,))
                yeast_id = c.lastrowid
            else:
                yeast_id = yeast_id[0]
            self.yeast[recipe.yeast] = yeast_id
        yeast_id = self.yeast[recipe.yeast]
        c.execute('INSERT INTO recipe_yeast(recipeID, yeastID) VALUES (?, ?)', (recipe_id, yeast_id,))

        # fermentables
        for fermentable in recipe.fermentables:
            try:
                if fermentable.name not in self.fermentables:
                    c.execute('SELECT id FROM fermentables WHERE name=(?)', (fermentable.name,))
                    fermentable_id = c.fetchone()
                    if not fermentable_id:
                        c.execute('INSERT INTO fermentables(name) VALUES (?)', (fermentable.name,))
                        fermentable_id = c.lastrowid
                    else:
                        fermentable_id = fermentable_id[0]
                    self.fermentables[fermentable.name] = fermentable_id
                fermentable_id = self.fermentables[fermentable.name]
                c.execute(
                    'INSERT INTO recipe_fermentables(recipeID, fermentableID, pounds) VALUES (?, ?, ?)',
                    (recipe_id, fermentable_id, fermentable.amount)
                )
            except sqlite3.IntegrityError:
                continue

        # hops
        for hop in recipe.hops:
            if hop.name not in self.hops:
                c.execute('SELECT id FROM hops WHERE name=(?)', (hop.name,))
                hop_id = c.fetchone()
                if not hop_id:
                    c.execute('INSERT INTO hops(name, alphaAcidPercentage) VALUES (?, ?)', (hop.name, 0,))
                    hop_id = c.lastrowid
                else:
                    hop_id = hop_id[0]
                self.hops[hop.name] = hop_id
            hop_id = self.hops[hop.name]
            c.execute(
                'INSERT INTO recipe_hops(recipeID, hopID, ounces, minutes) VALUES (?, ?, ?, ?)',
                (recipe_id, hop_id, hop.amount, hop.time)
            )
