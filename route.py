class Route:

    def __init__ (self,items,weight_left,volume_left,quant_left,opened,length):
        self.items = items 
        self.weight_left = weight_left
        self.volume_left = volume_left
        self.quant_left = quant_left
        self.opened = opened
        self.length = length

    def is_open (self):
        return self.opened

    def add_item (self,item,item_weight,item_volume,added_distance):
        # TODO Here an Item Class becomes handy
        self.items       += item
        self.weight_left -= item_weight
        self.volume_left -= item_volume
        self.quant_left  -= 1
        self.length      += added_distance
        if self.quant_left*self.volume_left*self.weight_left == 0:
            self.opened = False

    def accepts(self,item):
        pass