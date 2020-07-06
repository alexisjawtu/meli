import json
import random
import time
import sys


class TestCase(dict):


    def __init__(self, nItems = 10):

        self["demand"]        = []
        self["stock"]         = {}
        self.skus             = [self.rnd_sku() for i in range(nItems)]
        self.rnd_dispositions = [random.randint(1,5) for i in range(nItems)]
        for i in range(nItems):
            sku = self.rnd_sku()
            self["stock"][sku] = {
                self.rnd_label() : random.randint(1,10)
                for k in range(self.rnd_dispositions[i])
            }
            self["demand"] += [{
                "sku"    : sku,                     
                "weight" : random.randint(1,99),                   
                "volume" : random.randint(1,99)                       
            }]

    def rnd_label(self):

        aisle = random.randint(1,50)
        pos   = random.randint(1,140)
        aisle = "0"*(1+int(aisle<10)) + str(aisle)
        pos   = "0"*(int(pos<100)+int(pos<10)) + str(pos)
        return "MZ-1-{}-{}".format(aisle,pos)

    def rnd_sku(self):

        return ''.join([chr(random.randint(65,90)) for i in range(6)])

    def to_json(self,n):

        file_name = "demand_{}_{}.json".format(str(int(time.time())),n)
        with open (file_name,"w") as out:
            json.dump(self, out, indent=4)

def gen_test(n):

    for i in range(n):
        case = TestCase(random.randint(100,300))
        case.to_json(i)
        del(case)

if (__name__ == "__main__"):
    gen_test(int(sys.argv[1]))
