# meli

## Hypotheses assumed
1. There is a starting point, for all the routes, called ENTRANCE, at "MZ-1-000-000".
Distance from ENTRANCE to MZ-1-001-001 is 7 (1 aisle and 1 cross).
2. Users know the position labels and we only enumerate the picking order.
3. Everything adds 1 to the route distance (e.g. a rail in a cross aisle,
   moving from one box to another.)
4. There are no items in demand with the same sku.
5. Everything is in the same area, same floor.
6. There are additional single routes output because python dicts have unordered
keys.
7.  Collision Constraints
    1.  first phase: no three items in same aisle - block - side - picking_step,
        where 1 <= picking_step <= Route.QUANTITY 
{ 
    block-aisle-side-picking_turn : [] must have length < 3
}
side is odd or even.
8. in folder 4/ is the example where we had checked only "item collision"

## TODO List
0.  test and visualize the collision table behaviour running each individual test
in the console
1.  TAke care of the remaining items (when the last items collide
with everything in the past. Make turns for picking?)
1.  test jsons generator?
3.  Observe git messages convention!
4.  PERHAPS same--aisle--preference CONSTRAINTS
5.  if next closest crosses two cross aisles back, then mark as watched and
continue, to avoid ./avoid1.json UNLESS all the remaining items fit into the
current ROUTE! (the risk is to have an entire extra route for just one remaining
item.)
6. Should we take into account the distance from last item to EXIT?
