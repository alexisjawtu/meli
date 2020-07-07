import math
import random
import json
from   main import label_distance, ENTRANCE


class Output(dict):


    def sort (self):

        for turn, routes in iter(self.items()):
            # peek the first item picked in each route
            locs  = [route[0]["location"] for route in routes["routes"]]
            # sort measuring distance from the entrance
            order = sorted(range(len(locs)),
                           key     = lambda k : label_distance(locs[k],ENTRANCE),
                           reverse = True)
            routes["routes"] = [routes["routes"][j] for j in order]

    def to_json(self,json_in):

        with open ("{}_output".format(json_in[0:-5]),"w") as outfile:
            json.dump (self, outfile, indent = 4)

    def to_tex (self,json_in):

        file_name = "{}_output.tex".format(json_in[0:-5])
        color     = "color{}"
        item      = '\t\\fill[{}] ({},{}) circle (1.4ex);\n'
        node      = '\t\\node at  ({},{}) {};\n'

        text  = '\\documentclass[landscape]{article}\n\\usepackage{tikz}\n'
        text += '\\begin{document}\n'

        for n in self: # turns
            routes = self[n]["routes"]
            text  += '\n\\begin{figure}[htb]\n\\centering\\resizebox{\\textwidth}{!}{%\n'
            text  += '\\begin{tikzpicture}\n\t\\draw (0,0) circle (1.4ex);\n'
            text  += '\t\\node at (0,0) {E};\n'
            for m in range(len(routes)):
                color_name = color.format(m)
                r          = random.randint(1,255)
                g          = random.randint(1,255)
                b          = random.randint(1,255)
                tern       = "{"+"{},{},{}".format(r,g,b)+"}\n"
                text      +='\\definecolor{'+ color_name +'}{RGB}' + tern
                for obj in routes[m]:
                    x         = int(obj["location"][5:8])*4
                    x         = 0.05*x
                    position  = int(obj["location"][9:12])
                    y         = math.ceil(position/2) + 3*math.ceil(position/14)
                    y         = 0.05*(y-1)
                    this_item = item.format(color_name,x,y)
                    this_node = '\t\\node at  ({},{}) '.format(x,y) + '{' + str(m) +'};\n'
                    text     += this_item + this_node
            text += '\\end{tikzpicture}}\n\\end{figure}\n\\newpage'
        text = text[0:-8] +'\\end{document}'
        with open (file_name,'w') as d:
            d.write(text)
