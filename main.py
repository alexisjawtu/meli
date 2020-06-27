import math
from route import *

## items are pairs (sku,position_label,index_in_json)
## ruote.items = [(sku,pos_label), ..., (sku,pos_label)]
## I asume that an empty rout can load any single item

WEIGHT   = 1000
VOLUME   = 1000
QUANTITY = 100
ENTRANCE = "MZ-1-000-000"

def load (demand_json):
    with open (demand_json,'r') as f:
        d = json.load(f)
    return d

def listing (demand_dict):
    items_list = []
    guardar indice en la lista del json
    for sku in demand_dict:
        items_list += [(sku,position_label,json_idx) for position_label in d["stock"][sku]]

data          = load("demand.json")
demand, stock = (data["demand"], data["stock"])

demand_descr  = { i["sku"] : i for i in d['demand'] }

def check_eligible():
    check peso
    check vol
    check cantidad
    check colisiones

def label_distance (label_one, label_two):
    """ 
    labels are MZ-1-003-008: 
               area-floor-aisle-position 
    
    this distance takes everything as unitary
    and everything in same area -- same floor

                               { -1 if even - odd
    horizontal_correction    = {  0 if same parity
                               { +1 if odd - even
    """
    l = [label_one,label_two]
    l.sort()
    left, right = tuple(l)
    if left[5:8] == right[5:8] and int(left[9:12]) % 2 == 0:
        left, right = right, left
    aisles          = int(right[5:8]) - int(left[5:8])
    vert_pos_left, vert_pos_right = int(left[9:12]), int(right[9:12])
    layers        = [math.ceil(vert_pos_left/2),math.ceil(vert_pos_right/2)]
    diff_position = max(layers)-min(layers)
    horizontal_correction = vert_pos_left % 2 - vert_pos_right % 2
    crosses       = sum([int(i % 7 == 0) for i in range(min(layers),max(layers))])
    #print("aisles {}".format(aisles))
    #print("crosses {}".format(crosses))
    #print("horizontal_correction {}".format(horizontal_correction))
    #print("diff_position {}".format(diff_position))
        if crosses == 0 and aisles > 0:
        vertic_gap = min(layers[0] % 7 + layers[1] % 7, 16 - layers[0] % 7 - layers[1] % 7)
    else:
        vertic_gap = 3*crosses + diff_position
    horiz_gap = 4*aisles + horizontal_correction
    return vertic_gap + horiz_gap

def point_set_distance (current_label, other_labels):

    dist_realiz = other_labels[0]
    current_min = label_distance(dist_realiz,current_label)

    for label in other_labels:
        l_d = label_distance(label,current_label)
        if l_d < current_min:
            current_min = l_d
            dist_realiz = label

    return (dist_realiz,current_min)

def closest (item, items=[]):
    i = 0
    the_closest         = items[i]
    min_label, min_dist = distance(the_closest)
    i_min = i
    for k in range(i+1,len(items)):
        if items[k].get_in_stock:
            l, d = point_set_distance(item)
            if d < min_dist:
                min_label, min_dist = (l, d)
                i_min = k
    return i_min, min_dist

while len(demand) > 0:
    demand2 = copy demand
CONTINUE HERE ---> agregar un campo temporarily_watched en demand del json y poner
                 un if con eso en la local search y resetearlo cuando termina el ciclo de esa ruta
                 es mas, puedo poner temporarily_watched en todos los de igual sku porque el rechazo
                 va a ser por peso o volumen

    items       = listing(demand)
    actual_item = ("",ENTRANCE)
    route       = Route([],WEIGHT,VOLUME,QUANTITY,True)
--->demand_item_index, *stock_label_index*, min_distance = closest(actual_item, demand   items)
    
--->first_item = demand.pop(demand_item_index)<----
    # TODO Here an Item Class becomes handy
    weight = demand_descr[first_item[0]["weight"]]
    volume = demand_descr[first_item[0]["volume"]]
    route.add_item(first_item,weight,volume,min_distance)
    stock[first_item[0]][first_item[1]] -= 1
    if stock[first_item[0]][first_item[1]] == 0:
        stock[first_item[0]].pop(first_item[1])
--->#demand.pop()
    actual_item = first_item
    while route.is_open() and len(unwatched) > 0:
        #armo lista de tuplas temp = [(sku, pos_label), ... , (sku,pos_label)]
--->    min_item_index, min_distance = closest(actual_item,items)
        next_candidate = items[min_item_index]
        if route.accepts (next_candidate):
            ruta.agregar(+cercano)
            actual = +cercanos
            demand.pop(  )
            unwatched.
--->    else:
            unwatched.  falta algo que marque los que ya no sirvieron, sin borrarlos de la demanda

