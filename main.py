from algorithm import EditableParams, Calculator
from exampledata import G, Metric

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

editable_params: EditableParams = EditableParams(1, 1, 0.5, 10, 60, 0.1)

calculator: Calculator = Calculator(editable_params, connections.get_adjacency_matrix(), connections.get_metrics_matrix())
#calculator: Calculator = Calculator(editable_params, G, Metric)

calculator.run_aco_algorithm()
calculator.printInfo()
