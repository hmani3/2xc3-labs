import csv, math
from collections import defaultdict

class LondonTubeGraph():

    def __init__(self, csv_file):
        self.adj_list = defaultdict(list)
        self.load_csv(csv_file)

    def load_csv(self, csv_file):
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                station1, station2, distance = row
                distance = float(distance)
                self.graph[station1].append((station2, distance))
                self.graph[station2].append((station1, distance))

    def dijkstra(self, start, end):
        distances = {station: math.inf for station in self.graph}
        distances[start] = 0
        visited = set()
        while visited != set(self.graph.keys()):
            current_station = min((s for s in self.graph if s not in visited), key=lambda s: distances[s])
            visited.add(current_station)
            for neighbor, weight in self.graph[current_station]:
                if neighbor not in visited:
                    new_distance = distances[current_station] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
        return distances[end] if distances[end] != math.inf else None