


# Repo for abi-challenge


[Repo here](https://dev.azure.com/ErickCarvalho0358/_git/abi-challenge)


## Stack

* Python Django, Django Rest Framework
* Postgresql database
* Entities
    * locations
        * name
    * locations-map (Source -> Target: distance)
        * source: location 
        * target: location 
        * distance: int
    * vehicle-types
        * name: A, B, C
        * cargo_capacity: 10, 20, 30
    * vehicle
        * model: "F1000" <char>
        * vehicle_type: <vehicle-type id>
    * order
        * store: "Empório da cerveja" <char>
        * location: <location id>
        * quantity: int

* All endpoints:
    * /v1/locations/: CRUD Location
    * /v1/locations-map/: CRUD Mappings {source: location1, target: location2, distance: <int>}
    * /v1/vehicle-types/: CRUD Vehicle Type: A -> 10 Cargo Capacity
    * /v1/vehicle/: CRUD Vehicle 
    * /v1/order/: CRUD Order 
    * /v1/order/<int>/vehicle/ranking: Run Vehicle Score

## How to run

```bash

# Build container
$ make build

# Start application
$ make up
# Application will be up on port :8000

# Run test
# Test is at order/tests.py
$ make test
# This will run the test based on the question data
# Result
[
    {
	"id_vehicle": 4,
        "model": "F1000",
        "location": "B",
        "capacity": 40,
        "score": 87.5
	},
    {
	"id_vehicle": 1,
        "model": "F1000",
        "location": "C",
        "capacity": 20,
        "score": 62.5
	},
    {
	"id_vehicle": 2,
        "model": "F1000",
        "location": "E",
        "capacity": 20,
        "score": 50
	}
]

```

## Vehicle score

The algorithm for vehicle scoring is located at: `core/algo.py`

The shortest path algorithm is a BFS Breadth first search with a few tweaks
to work with our dataset.

Its runtime complexity is nearly O(n*m) where *m* corresponds to all the entries 
in our mapping table. It's worse compared to other
shortest path finder algorithms due to the way we've stored the graph 
in the database structured as:

| source | target | distance |
| --- | --- | --- |
| A | B | 10 |
| C | D | 20 |

So to get a list of all the neighbours of a location A we'll have to iterate
through all the entries to filter those where its source or target value
is A.

One way to optimize this is by pre structuring the generated whenever a
new location entry is added. We could do this by using 
[Django signals](https://docs.djangoproject.com/en/3.1/topics/signals/) and 
store it in some known location for later use by our algorithm.

So from our order store location we start the BFS iterating and updating
the shortest path distance amongst all its neighbours as show in the 
code below.

```python
  1     def _bfs_search_from_target(self, graph, target):
  2         def find_neighbours(g_, t_):
  3             ret = {}
  4             for g in g_:
  5                 n = ""
  6                 d = g["distance"]
  7                 if g["source"] == t_:
  8                     n = g["target"]
  9                 elif g["target"] == t_:
 10                     n = g["source"]
 11
 12                 if n != "":
 13                     ret[n] = min(d, ret.get(n, d))
 14             return ret
 15
 16         queue = set()
 17         queue.add(target)
 18         visited = set()
 19         ret = {target: 0}
 20
 21         while len(queue) != 0:
 22             node = queue.pop()
 23             if node in visited: continue
 24             visited.add(node)
 25             neighs = find_neighbours(graph, node)
 26             for neigh,dist in neighs.items():
 27                 prev_dist = ret.get(node, 0)
 28                 ret[neigh] = min(prev_dist+dist,
 29                                  ret.get(neigh, prev_dist+dist))
 30                 queue.add(neigh)
 31
 32
 33         return ret
```

