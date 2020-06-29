import math

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
    l = [label_one,label_two]
    l.sort()
    left, right = tuple(l)
    if left[5:8] == right[5:8] and int(left[9:12]) % 2 == 0:
        left, right = right, left
    #aisle_pair      = [int(left[5:8]), int(right[5:8])]
    aisles          = int(right[5:8]) - int(left[5:8])
    vert_pos_left, vert_pos_right = int(left[9:12]), int(right[9:12])
    layers        = [math.ceil(vert_pos_left/2),math.ceil(vert_pos_right/2)]
    diff_position = max(layers)-min(layers)
    horizontal_correction = vert_pos_left % 2 - vert_pos_right % 2
    crosses       = sum([int(i % 7 == 0) for i in range(min(layers),max(layers))])
    print("aisles {}".format(aisles))
    print("crosses {}".format(crosses))
    print("horizontal_correction {}".format(horizontal_correction))
    print("diff_position {}".format(diff_position))
    if crosses == 0 and aisles > 0:
        vertic_gap = min(layers[0] % 7 + layers[1] % 7, 16 - layers[0] % 7 - layers[1] % 7)
    else:
        vertic_gap = 3*crosses + diff_position
    horiz_gap = 4*aisles + horizontal_correction
    return vertic_gap + horiz_gap

print("a MZ-1-001-007 ... MZ-1-001-021:")
print(str(label_distance("MZ-1-001-007","MZ-1-001-021"))+"\n")

print("b MZ-1-004-010 ... MZ-1-006-030:")
print(str(label_distance("MZ-1-004-010","MZ-1-006-030"))+"\n")

print("c MZ-1-005-021 ... MZ-1-005-021:")
print(str(label_distance("MZ-1-005-021","MZ-1-005-021"))+"\n")

print("d MZ-1-005-019 ... MZ-1-005-023:")
print(str(label_distance("MZ-1-005-019","MZ-1-005-023"))+"\n")

print("e MZ-1-001-039 ... MZ-1-003-009:")
print(str(label_distance("MZ-1-001-039","MZ-1-003-009"))+"\n")

print("f MZ-1-004-037 ... MZ-1-002-035:")
print(str(label_distance("MZ-1-004-037","MZ-1-002-035"))+"\n")

print("g MZ-1-004-035 ... MZ-1-002-031:")
print(str(label_distance("MZ-1-004-035","MZ-1-002-031"))+"\n")

print("h MZ-1-004-033 ... MZ-1-004-034:")
print(str(label_distance("MZ-1-004-033","MZ-1-004-034"))+"\n")

print("i MZ-1-001-025 ... MZ-1-001-024:")
print(str(label_distance("MZ-1-001-025","MZ-1-001-024"))+"\n")

print("j MZ-1-002-022 ... MZ-1-002-019:")
print(str(label_distance("MZ-1-002-022","MZ-1-002-019"))+"\n")

print("k MZ-1-004-021 ... MZ-1-003-022:")
print(str(label_distance("MZ-1-004-021","MZ-1-003-022"))+"\n")

print("l MZ-1-005-010 ... MZ-1-006-009:")
print(str(label_distance("MZ-1-005-010","MZ-1-006-009"))+"\n")




{

'S58GAK': 
 {'weight': 20, 'volume': 30, 'etd': '2020-03-20T14:20:00.000-03:00', 'sku': 'S58GAK'},
'ASYQU8': 
 {'weight': 10, 'volume': 40, 'etd': '2020-03-20T14:40:00.000-03:00', 'sku': 'ASYQU8'}

}



First version of greedy backtracking approach running.
Started testing.
now temporary items are dicts with the collected fields from "demand" and "stock" out of the json.

TODO: put constants weight etc, and do the overall math with weight instead of
weight_left 
TODO: " ".format() the __str__ output




