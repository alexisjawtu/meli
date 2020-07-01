class Item:

    def __init__(self,position_label):

        ## WHEN IMPLEMENTING THIS beware of layers and other stuff
        ## starting at 0 or 1

        self.label = position_label
        self.layer = math.ceil(int(stock_label[9:12])/2) - 1
        self.block = divmod(layer,7)
        self.aisle = stock_label[5:8]