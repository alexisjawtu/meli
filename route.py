class Route:

    WEIGHT   = 99
    VOLUME   = 199
    QUANTITY = 5

    def __init__ (self,number,items,weight,volume,quant,length,opened):
        self.number = number
        self.items  = items # [(sku,position)]
        self.weight = weight
        self.volume = volume
        self.quant  = quant
        self.length = length
        self.opened = opened

    def __str__(self):
        head = "Cantidad: {}. Peso: {}. Volumen: {}. Distancia a recorrer hasta el item final: {}.\n\n"
        head = head.format(str(self.quant),str(self.weight),\
                 str(self.volume),str(self.length))
        body = ''
        for i in range(len(self.items)):
            body += "{}. Pos: {}, sku: {}\n".format(i+1,self.items[i][1],self.items[i][0])
        return head + body

    def to_txt (self):
        with open ("ruta_{}.txt".format(self.number),"w") as out:
            out.write("RUTA {}\n".format(self.number))
            out.write(str(self))

    def to_json (self):
        return {
            position : sku
            for sku, position in self.items 
        }

    def is_open (self):
        return self.opened

    def add_item (self,item):
        # TODO Here an Item Class becomes handy
        self.items  += [(item["sku"],item["stock_label"])] 
        self.weight += item["weight"]
        self.volume += item["volume"]
        self.quant  += 1
        self.length += item["added_distance"]
        if self.quant == self.QUANTITY or self.volume == self.VOLUME \
            or self.weight == self.WEIGHT:
            self.opened = False

    def accepts(self,item):
        x = item["weight"] + self.weight <= self.WEIGHT
        x = x and item["volume"] + self.volume <= self.VOLUME
        #check colisiones
        return x
