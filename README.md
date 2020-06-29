# meli

## Hypotheses assumed
1. All the single items fit into one empty route.
2. There is a starting point, for all the routes, called ENTRANCE.
3. Users know the position labels and we only enumerate the picking order.
4. Everything adds 1 to the route distance (e.g. a rail in a cross aisle,
   moving from one box to another.)
5. There are no items in demand with the same sku.
6. Everything is in the same area, same floor.

## TODO List
1.  test by hand small instances to check the distances
2.  COLLISION CONSTRAINTS
3.  think about the objective functions Alejandro said
4.  PERHAPS same--aisle--preference CONSTRAINTS
5.  if next closest crosses two cross aisles back, then mark as watched and
continue, to avoid ./avoid1.json
6.  put constants weight etc, and do the overall math with weight instead of
weight_left
7. Put constants named: box, rails, etc, all equal to 1,
to measure distance more flexible