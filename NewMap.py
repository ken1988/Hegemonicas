'''
Created on 2015/05/07

@author: ken
'''
class MakeMap(webapp2.RequestHandler):

    def get(self):

        terrain = ["Sea","Plain","Mountain"]
        architect = ['Town','Farm','None','None','None','None','None','None']
        reader=csv.reader(open('test-map.csv'))

        locy = 0
        for row in reader:
            locx = 0

            for column in row:
                column = int(column)
                newName = "X" + str(locx) +":Y" + str(locy)
                newMap = MapChip(key_name = newName)
                newMap.locationX = locx
                newMap.locationY = locy
                newMap.terra = terrain[column]

                if newMap.terra == "Plain":
                    arc = random.choice(architect)
                    newMap.architect = arc
                    if arc == "Town":
                        newMap.pop = 100
                newMap.put()

                template_values = {
                                   'locationX': newMap.locationX,
                                   'locationY': newMap.locationY,
                                   'terra'    : newMap.terra,
                                   'architect': newMap.architect,
                                   'pop'      : newMap.pop,
                                   }

                path = os.path.join(os.path.dirname(__file__), './templates/MapMaker.html')
                self.response.out.write(template.render(path, template_values))
                locx = locx + 1

            locy = reader.line_num