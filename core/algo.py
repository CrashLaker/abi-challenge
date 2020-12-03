import pprint
import json




class Algo:

    closest_neighbours = []

    def __init__(self, graph, vehicles, order):
        # graph would be the map. arr of:
        # {"source": "A", "target": "B", distance: 20}
        self.graph = graph

        # need vehicles cargo_capacity
        # dict("model", "capacity", "location", "id_vehicle")
        self.vehicles = vehicles

        # order detail dict
        # dict("id", "quantity", "location")
        self.order = order

    def boilerplate(self):
        self.closest_neighbours = self._bfs_search_from_target(
            self.graph, 
            self.order['location']
        )
        return self

    def get_score_list(self):

        for vehicle in self.vehicles:
           vehicle["score"] = self._get_score(vehicle) 

        self.vehicles = sorted(self.vehicles, 
                               key=lambda x: x["score"],
                               reverse=True)

        return self.vehicles
    
    def _get_score(self, vehicle):
        # nb is the amount of boxes of beer an store requested
        # nc is the vehicle delivery capacity
        nb = self.order["quantity"]
        nc = vehicle["capacity"]
        n = 100 - 25 * abs((nb-nc)/10)
        d = self._score_d(vehicle["location"])
        return (n+d)/2

    def _score_d(self, vehicle_loc):
        if vehicle_loc not in self.closest_neighbours: # no path found
            return 0

        dist = self.closest_neighbours[vehicle_loc]
        ans = 0
        if dist <= 5:    ans = 100
        elif dist <= 10: ans = 75
        elif dist <= 15: ans = 50
        elif dist <= 20: ans = 25
        else:            ans = 0

        return ans

    def _bfs_search_from_target(self, graph, target):
        def find_neighbours(g_, t_):
            ret = {}
            for g in g_:
                n = ""
                d = g["distance"]
                if g["source"] == t_:
                    n = g["target"]
                elif g["target"] == t_:
                    n = g["source"]
                
                if n != "":
                    ret[n] = min(d, ret.get(n, d))
            return ret

        queue = set()
        queue.add(target)
        visited = set()
        ret = {target: 0}
        
        while len(queue) != 0:
            node = queue.pop()
            if node in visited: continue
            visited.add(node)
            neighs = find_neighbours(graph, node)
            for neigh,dist in neighs.items():
                prev_dist = ret.get(node, 0)
                ret[neigh] = min(prev_dist+dist, 
                                 ret.get(neigh, prev_dist+dist))
                queue.add(neigh)

           
        return ret
        




if __name__ == '__main__':
    vehicles = [
        {"model": "F1000", "cargo_capacity": 40, "location": "B"},
        {"model": "F1000", "cargo_capacity": 20, "location": "C"},
        {"model": "F1000", "cargo_capacity": 20, "location": "E"},
    ]

    graph = [
        {"source": "A", "target": "B", "distance": 5},
        {"source": "B", "target": "C", "distance": 7},
        {"source": "B", "target": "D", "distance": 3},
        {"source": "C", "target": "E", "distance": 4},
        {"source": "D", "target": "E", "distance": 10},
        {"source": "D", "target": "F", "distance": 8},
    ]

    order = {
        "name": "Empório da Cerveja",
        "location": "A",
        "quantity": 30
    }


    algo = Algo(graph, vehicles, order)

    algo.boilerplate()
    score = algo.get_score_list()
    print(json.dumps(score))






