import math
from route import *

def label_distance (label_one, label_two):
    """ 
    labels are MZ-1-003-008: 
                   area-floor-aisle-position 
    this distance takes everything as unitary

                                { -1 if even--odd
    horizontal_correction     = {  0 if same parity
                                { +1 if odd--even
    """

    pos             = [int(label_one[9:12]), int(label_two[9:12])]
    layers          = [math.ceil(pos[0]/2),math.ceil(pos[1]/2)]

    diff_position   = max(layers)-min(layers)

    print("diff_position {}".format(diff_position))
    aisles          = math.fabs(int(label_one[5:8]) - int(label_two[5:8]))
    print("aisles {}".format(aisles))
    horizontal_correction = (pos[0] % 2 - pos[1] % 2)
    print("horizontal_correction {}".format(horizontal_correction))
    crosses         = sum([int(i % 7 == 0) for i in range(min(layers),max(layers))])
    print("crosses {}".format(crosses))

    # check if both are between same crosses. Not so readable. Fix.
    turn        = min(layers[0] % 7 + layers[1] % 7, 16 - layers[0] % 7 - layers[1] % 7)
    cross_gap   = turn*int(crosses == 0) + int(crosses != 0)*(3*crosses + diff_position)
    return cross_gap + 4*aisles + horizontal_correction
