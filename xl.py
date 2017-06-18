
# parse through excel sheet to make lists of the data 
# then use the lists to create a bird class with its data as instance variables

from xlrd import open_workbook

wb = open_workbook('ML_Birds_2017_June.xls')

catalog = [] #this holds all the catalog IDs (for url/dl parsing)
common_names = [] #holds all common names (for presentation / image)
sci_names = []  #holds the scientific names (for presentation)
recordists = [] #holds the recordist names (for credits)
location = []
#?maybe consider adding location too

for s in wb.sheets():
    for i in range(1, s.nrows): #this is the row we are on
       
        catalog_number = str(int(s.cell_value(i,0)))
        catalog.append(catalog_number) #this holds all the catalog numbers

        common = str(s.cell_value(i, 3))
        scientific = str(s.cell_value(i, 2))   #!make sure to check on the exceptions and repeats (without ruining the list)
        common_names.append(common) 
        sci_names.append(scientific)

        recordist = str(s.cell_value(i, 6))
        recordists.append(recordist)    #?may want to randomize output a bit

        loc = str(s.cell_value(i,12))
        location.append(loc)

class Bird(object):

    def __init__(self, index):
        self.id = catalog[index]
        self.common = common_names[index]
        self.scientific = sci_names[index]
        self.credit = recordists[index]
        self.loc = location[index]

    def get_Bird_ID():
        return self.id

    def get_loc():
        return self.loc
