# meli

## Hypotheses assumed
1. There is a starting point, for all the routes, called ENTRANCE, at "MZ-1-000-000".
Distance from ENTRANCE to MZ-1-001-001 is 7 (1 aisle and 1 cross).
2. There is an order of departure for the routes, 
given by the position of their first pick, which leads to some sort
of First In First Out situation.
3. output.json is a list of turns, each turn is a list of routes
4. Users know the position labels and we only enumerate the picking order.
5. Everything adds 1 to the route distance (e.g. a rail in a cross aisle,
   moving from one box to another.)
6. There are no items in demand with the same sku.
7. Everything is in the same area, same floor.
8.  Collision Constraints
    1.  first phase: no three items in same aisle - block - side - picking_step,
        where 1 <= picking_step <= Route.QUANTITY 
{ 
    block-aisle-side-picking_turn : [] must have length < 3
}
side is odd or even.
9. output := { 
        turn1 : { "routes" : [ []. [], [] ] },
        turn2 : { "routes" : [] }
     }


## Study Cases
1. in folder 7/ we test a demand all collapsed within th first block,
aisles 1 to 3. Observe how the routes don't collide.
   1.  Routes 7 and 8 in separate halves of aisle 3
   2.  Routes 4 and 6 in separate halves of aisle 2
   3.  Routes 1 and 2 in different sides of aisle 1
   4.  Routes 3 and 5 in different halves of aisles 1 and 2
2. in folder 8/ we included the reversed order to avoid pickers 
blocking other pickers heading to more advanced boxes in the same aisle/block.
3. in folder 4/ is the example where we had checked only "item collision"

## TODO List
0.  test and visualize the collision table behaviour running each individual test
in the console
1.  test jsons generator?
2.  Observe git messages convention!
3.  PERHAPS same--aisle--preference CONSTRAINTS
4.  if next closest crosses two cross aisles back, then mark as watched and
continue, to avoid ./avoid1.json UNLESS all the remaining items fit into the
current ROUTE! (the risk is to have an entire extra route for just one remaining
item.)
5. Should we take into account the distance from last item to EXIT?
