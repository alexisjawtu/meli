import math

## ruta = [(sku,pos_label), ..., (sku,pos_label)]

while len(demanda) > 0:
    ruta            = []
    resto peso      = PESO_MAX
    resto vol       = MAX_VOL
    resto cantidad  = MAX_CANT
    actual          =  closest a la entrada
    while ruta.get_open():
        armo lista de tuplas temp = [(sku, pos_label1,...,pos_labeln)]
        pispeo en temp el mas cercano a actual
            (tengo que tener el indice donde esta el mas proximo)
        si sirve():
            ruta.agregar(+cercano)
            actual = +cercanos
        temp.pop()


sirve():
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

def closest (items=[]):
    i = 0
    #while items[i].picked == True:
    #    i += 1
    the_closest         = items[i]
    min_label, min_dist = distance(****)
    i_min = i
    for k in range(i+1,len(items)):
        if items[k].get_in_stock:
            l, d = distance(item)
            if d < min_dist:
                min_label, min_dist = (l, d)
                i_min = k
    #the_closest = items[i_min]
    #the_closest.set_routed_label(l)
    return i_min, min_label, min_dist

