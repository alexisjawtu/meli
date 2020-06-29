class Route:

    def __init__ (self,items,weight_left,volume_left,quant_left,length,opened):
        self.items = items # [(sku,position)]
        self.weight_left = weight_left
        self.volume_left = volume_left
        self.quant_left = quant_left
        self.length = length
        self.opened = opened

    def __str__(self):
        head = "Cantidad: {}. Peso: {}. Volumen: {}. Distancia a recorrer: {}.\n\n"
        head = head.format(str(self.quant_left),str(self.weight_left),\
                 str(self.volume_left),str(self.length))
        body = ''
        for i in range(len(self.items)):
            body += "{}. Pos: {}, sku: {}\n".format(i+1,self.items[i][1],self.items[i][0])
        return head + body

    def to_txt (self, route_number):
        with open ("ruta_{}.txt".format(route_number),"w") as out:
            out.write("RUTA {}\n".format(route_number))
            out.write(str(self))

    def is_open (self):
        return self.opened

    def add_item (self,item):
        # TODO Here an Item Class becomes handy
        self.items       += [(item["sku"],item["stock_label"])] 
        self.weight_left -= item["weight"]
        self.volume_left -= item["volume"]
        self.quant_left  -= 1
        self.length      += item["added_distance"]
        if self.quant_left*self.volume_left*self.weight_left == 0:
            self.opened = False

    def accepts(self,item):
        x = True
        x = x and item["weight"] < self.weight_left
        x = x and item["volume"] < self.volume_left
        #check colisiones
        return x
