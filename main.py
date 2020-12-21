
from connections import ConnectionGraph

connections: ConnectionGraph = ConnectionGraph()

connections.append("IP 1", "IP 2", 2)
connections.append("IP 2", "IP 3", 2)
connections.append("IP 3", "IP 4", 2)
connections.append("IP 4", "IP 5", 2)
connections.append("IP 6", "IP 4", 2)
connections.append("IP 5", "IP 1", 2)
connections.append("IP 5", "IP 2", 2)

print(connections.get_adjacency_matrix())
print(connections.get_metrics_matrix())

