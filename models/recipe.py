class Recipe:

    name = ''
    style = ''
    og = 0
    fg = 0
    ibu = 0
    srm = 0
    yeast = ''
    hops = []
    fermentables = []

    def __init__(self, name):
        self.name = name
        self.style = ''
        self.og = 0
        self.fg = 0
        self.ibu = 0
        self.srm = 0
        self.yeast = ''
        self.hops = []
        self.fermentables = []
