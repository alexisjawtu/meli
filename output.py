

class Output(dict):


    def sort (self):

        for turn, routes in iter(self.items()):
            locs  = [route[0]["location"] for route in routes["routes"]]
            order = sorted(range(len(locs)),
                           key     = lambda k : locs[k],
                           reverse = True)
            routes["routes"] = [routes["routes"][o] for o in order]
