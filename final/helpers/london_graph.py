import csv, math
from collections import defaultdict

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

class LondonTubeGraph():

    def __init__(self):
        # adj_list[station_id] = (neighbour_id, time, line)
        self.adj_list = defaultdict(list)

        # station_info[station_id] = {name,lat,lon,zone,total_lines,display,rail}
        self.station_info = {}

    def load_stations(self, stations_file):
        """Read londan_stations.csv, load station information to station_info"""
        with open(stations_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station_id = int(row['id'])
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
                # stations are nodes 'u', 'v'
                u = int(row['station1'])
                v = int(row['station2'])
                # weight by time for edge, in minutes from u to v or v to u
                weight = int(row['time'])
                # line taken (wil be used for analysis)
                line = int(row['line'])
                
                # Tube connections are bidirectional (undirected graph, we can go both ways for any 2 stations)
                self.adj_list[u].append((v, weight, line))
                self.adj_list[v].append((u, weight, line))

    def get_neighbors(self, station_id):
        return self.adj_list[station_id]
    def get_coords(self, station_id):
        return self.station_info[station_id]['lat'], self.station_info[station_id]['lon']
    
    def calculate_max_speed(self):
        # calculate the maximum speed of travel in km / min across all connections, to be used in heuristic calculation
        max_speed_kmm = 0
        for u in self.adj_list:
            lat1, lon1 = self.get_coords(u)
            for v, weight, line in self.adj_list[u]:
                if weight > 0:
                    lat2, lon2 = self.get_coords(v)
                    distance_km = haversine_distance(lat1, lon1, lat2, lon2)
                    speed_kmm = (distance_km / weight)
                    if speed_kmm > max_speed_kmm: max_speed_kmm = speed_kmm
        return max_speed_kmm
    
    def calculate_heuristic(self, station_id1, station_id2, max_speed_kmm):
        """Calculate heuristic (straight-line distance) between two stations using their lat/lon coordinates for haversine distance
            as well as max potential speed in km / min."""
        lat1, lon1 = self.get_coords(station_id1)
        lat2, lon2 = self.get_coords(station_id2)
        
        #  return the time it would take to travel the straight line distance at max speed, as a heuristic for A* search
        return  haversine_distance(lat1, lon1, lat2, lon2) / max_speed_kmm if max_speed_kmm > 0 else float('inf')
    
    def print_graph(self, limit=5):
        """
        Prints a neat summary of the graph's nodes and edges.
        By default, we limit the output to the first 5 stations to avoid flooding the console.
        """
        # Calculate total unique edges (divide by 2 since it's an undirected graph)
        total_edges = sum(len(neighbors) for neighbors in self.adj_list.values()) // 2
        
        print(f"--- Graph Summary ---")
        print(f"Total Stations (Nodes): {len(self.station_info)}")
        print(f"Total Connections (Edges): {total_edges}")
        print("-" * 50)
        
        count = 0
        for station_id, info in self.station_info.items():
            if limit is not None and count+1 > limit:
                print(f"\n... and {len(self.station_info) - limit} more stations.")
                break
                
            print(f"[{station_id}] {info['name']} (Zone {info['zone']})")
            
            neighbors = self.adj_list.get(station_id, [])
            if not neighbors:
                print("  -> (No connections found)")
            else:
                for neighbor_id, time_weight, line in neighbors:
                    # Fetch the neighbor's name for a more readable output
                    neighbor_name = self.station_info[neighbor_id]['name']
                    print(f"  -> to {neighbor_name} (ID: {neighbor_id}) | Time: {time_weight} mins | Line ID: {line}")
            
            print() # Blank line for visual separation
            count += 1

