import math
from route import *

def label_distance (label_one, label_two):
    """ 
    labels are MZ-1-003-008: 
                   area-floor-aisle-position 
    this distance takes everything as unitary

                               { -1 if even - odd
    horizontal_correction    = {  0 if same parity
                               { +1 if odd - even
    """
    ## Assuming we are always in the same area-floor
    left, right = tuple([label_one,label_two].sort())
    if left[5:8] == right[5:8] and int(left[9:12]) % 2 == 0:
        left, right = right, left
    #aisle_pair      = [int(left[5:8]), int(right[5:8])]
    aisles          = int(right[5:8]) - int(left[5:8])
    print("aisles {}".format(aisles))
    vert_pos_left, vert_pos_right = int(left[9:12]), int(right[9:12])
    layers        = [math.ceil(vert_pos_left/2),math.ceil(vert_pos_right/2)]
    diff_position = max(layers)-min(layers)
    print("diff_position {}".format(diff_position))
    horizontal_correction = vert_pos_left % 2 - vert_pos_right % 2
    print("horizontal_correction {}".format(horizontal_correction))
    crosses       = sum([int(i % 7 == 0) for i in range(min(layers),max(layers))])
    print("crosses {}".format(crosses))
    if crosses == 0 and aisles > 0:
        vertic_gap = min(layers[0] % 7 + layers[1] % 7, 16 - layers[0] % 7 - layers[1] % 7)
    else:
        vertic_gap = 3*crosses + diff_position
    horiz_gap = 4*aisles + horizontal_correction
    return vertic_gap + horiz_gap



print("1 MZ-1-001-007 ... MZ-1-001-021: {}".format(label_distance("MZ-1-001-007","MZ-1-001-021")))
print("2 MZ-1-004-010 ... MZ-1-006-030: {}".format(label_distance("MZ-1-004-010","MZ-1-006-030")))
print("3 MZ-1-005-021 ... MZ-1-005-021: {}".format(label_distance("MZ-1-005-021","MZ-1-005-021")))
print("4 MZ-1-005-019 ... MZ-1-005-023: {}".format(label_distance("MZ-1-005-021","MZ-1-005-023")))
print("5 MZ-1-001-039 ... MZ-1-003-009: {}".format(label_distance("MZ-1-001-039","MZ-1-003-009")))
print("6 MZ-1-004-037 ... MZ-1-002-035: {}".format(label_distance("MZ-1-004-037","MZ-1-002-035")))
print("7 MZ-1-004-033 ... MZ-1-002-031: {}".format(label_distance("MZ-1-004-033","MZ-1-002-031")))
print("8 MZ-1-004-033 ... MZ-1-004-034: {}".format(label_distance("MZ-1-004-033","MZ-1-004-032")))


