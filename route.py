import math


class Route:


    WEIGHT   = 499
    VOLUME   = 499
    QUANTITY = 10

    def __init__ (self,number,items,weight,volume,quantity,length,opened):

        self.number   = number
        self.items    = items 
        self.weight   = weight
        self.volume   = volume
        self.quantity = quantity
        self.length   = length
        self.opened   = opened

    def __str__(self):

        head  = "Cantidad: {}. Peso: {}. Volumen: {}. "
        head += "Distancia a recorrer hasta el item final: {}.\n\n"
        head  = head.format(str(self.quantity),str(self.weight),\
                            str(self.volume),str(self.length))
        body = ''
        for i in range(len(self.items)):
            body += "{}. Pos: {}, sku: {}\n".format(i+1,
                                                    self.items[i]["location"],
                                                    self.items[i]["sku"])
        return head + body

    def to_txt (self):

        with open ("ruta_{}.txt".format(self.number),"w") as out:
            out.write("RUTA {}\n".format(self.number))
            out.write(str(self))

    def to_json (self):
        return [
                   {
                       "sku"       : i["sku"],
                       "quantity"  : i["quantity"],
                       "location"  : i["location"]
                   }
                   for i in self.items[1:]
               ]

    def is_open (self):

        return self.opened

    def add_item (self,item):

        self.items    += [
                            {
                                "sku"      : item["sku"],
                                "location" : item["location"],
                                "quantity" : item["quantity"],
                                "weight"   : item["weight"],
                                "volume"   : item["volume"]
                            }
                         ]

        self.weight   += item["weight"]
        self.volume   += item["volume"]
        self.quantity += 1
        self.length   += item["added_distance"]
        if (self.quantity == self.QUANTITY or self.volume == self.VOLUME
                or self.weight == self.WEIGHT):
            self.opened = False

    def accepts(self,item):

        x          = item["weight"] + self.weight <= self.WEIGHT
        x          = x and item["volume"] + self.volume <= self.VOLUME
        last_block = math.ceil(int(self.items[-1]["location"][9:12])/14)
        last_aisle = int(self.items[-1]["location"][5:8])
        block      = math.ceil(int(item["location"][9:12])/14)
        if (last_block - block > 1):  ## vertical zigzag bound
            x = x and False
            #print("vertical zigzag bound triggered")
        aisle      = int(item["location"][5:8])
        #if (math.fabs(last_aisle - aisle) > 2): ## horiz zigzag bound
        #    print("horiz zigzag bound triggered")
        #    x = x and False
        return x
