import csv, math
from graphs import DirectedWeightedGraph

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the  distance in km between two points w lat lon, use in heurestic."""
    R = 6371.0  # Earth radius in kilometers
    lat1_rad, lat2_rad = math.radians(lat1), math.radians(lat2)
    lon1_rad, lon2_rad = math.radians(lon1), math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

class LondonTubeGraph(DirectedWeightedGraph):

    def __init__(self):
        super().__init__()
        # station_info[station_id] = {name,lat,lon,zone,total_lines,display,rail}
        self.station_info = {}
        self.lines = {}

    def load_stations(self, stations_file):
        """Read londan_stations.csv, load station information to station_info"""
        with open(stations_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station_id = int(row['id'])
                
                # add station_id node to dwg
                self.add_node(station_id)
                
                self.station_info[station_id] = {
                    'name': row['name'],
                    'lat': float(row['latitude']),
                    'lon': float(row['longitude']),
                    'zone': float(row['zone']) if row['zone'] else None,
                    'total_lines': int(row['total_lines']),
                    'display': str(row['display_name']) if row['display_name'] else None,
                    'rail' : False if row['rail'] == 0 else True
                }

    def load_connections(self, connections_file):
        """Read london_connections.csv to build weighted edges"""
        with open(connections_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                u = int(row['station1'])
                v = int(row['station2'])
                weight = int(row['time'])
                line = int(row['line'])
                
                # Use parent methods to add bidirectional edgese
                self.add_edge(u, v, weight)
                self.add_edge(v, u, weight)
                
                # Store the line information in custom dictionary (analysis)
                self.lines[(u, v)] = line
                self.lines[(v, u)] = line

    def get_coords(self, station_id):
        return self.station_info[station_id]['lat'], self.station_info[station_id]['lon']
    
    def calculate_max_speed(self):
        """ calculate the maximum speed of travel in km / min across all connections, to be used in heuristic calculation """
        max_speed_kmm = 0
        best = (-1, -1, -1)
        
        # Iterate over self.adj from the parent class
        for u in self.adj:
            lat1, lon1 = self.get_coords(u)
            for v in self.adj[u]:
                weight = self.w(u, v) # Fetch weight using parent method
                line = self.lines[(u, v)]
                
                if weight > 0:
                    lat2, lon2 = self.get_coords(v)
                    distance_km = haversine_distance(lat1, lon1, lat2, lon2)
                    speed_kmm = (distance_km / weight)
                    if speed_kmm > max_speed_kmm: 
                        best = (u, v, line)
                        max_speed_kmm = speed_kmm
        return (max_speed_kmm, best)
    

    # HEURISTIC CALCULATION
    
    def calculate_heuristic(self, station_id1, station_id2, max_speed_kmm):
        """Calculate heuristic (straight-line distance) between two stations using their lat/lon coordinates for haversine distance
            as well as max potential speed in km / min."""
        lat1, lon1 = self.get_coords(station_id1)
        lat2, lon2 = self.get_coords(station_id2)

        #  return the time it would take to travel the straight line distance at max speed, as a heuristic for A* search
        dis = haversine_distance(lat1,lon1,lat2,lon2)
        return  (dis / max_speed_kmm) if max_speed_kmm > 0 else float('inf')

    def create_heuristic_dict(self):
        """ returns a dictionary res where res[u] = the heurestic function starting at node u """
        res = dict()
        max_speed, _ = self.calculate_max_speed()

        for start_node in self.station_info.keys():
            h = dict()
            for destination_node in self.station_info.keys():
                h[destination_node] = self.calculate_heuristic(start_node, destination_node, max_speed)
            res[start_node] = h
        return res

    # PRINT GRAPH
    
    def print_station(self,station_id):
        """ Print for testing and debugging"""
        info = self.station_info[station_id]
        print(f"[{station_id}] {info['name']} (Zone {info['zone']})")
        
        neighbors = self.adj.get(station_id, [])
        if not neighbors:
            print("  -> (No connections found)")
        else:
            for neighbor_id in neighbors:
                weight = self.w(station_id, neighbor_id)
                line = self.lines[(station_id, neighbor_id)]
                neighbor_name = self.station_info[neighbor_id]['name']
                print(f"  -> to {neighbor_name} (ID: {neighbor_id}) | Time: {weight} mins | Line ID: {line}")


    def print_graph(self, limit=5):
        """
        Prints a neat summary of the graph's nodes and edges.
        By default, we limit the output to the first 5 stations to avoid flooding the console.
        """
        # Calculate total unique edges (divide by 2 since it's an undirected graph)
        total_edges = sum(len(neighbors) for neighbors in self.adj.values()) // 2
        
        print(f"--- Graph Summary ---")
        print(f"Total Stations (Nodes): {self.number_of_nodes()}")
        print(f"Total Connections (Edges): {total_edges}")
        print("-" * 50)
        
        count = 0
        for station_id in self.station_info.keys():
            if limit is not None and count + 1 > limit:
                print(f"\n... and {self.number_of_nodes() - limit} more stations.")
                break
            self.print_station(station_id)
            print() 
            count += 1
