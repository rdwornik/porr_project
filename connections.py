from typing import List, Optional

from model import NetworkConnection


class ConnectionGraph:
    def __init__(self):
        self.connections: List[NetworkConnection] = []
        self.ips: List[str] = []

    def append(self, first: str, second: str, metric: int):
        if not self.ips.__contains__(first):
            self.ips.append(first)
        if not self.ips.__contains__(second):
            self.ips.append(second)
        self.connections.append(
            NetworkConnection(
                self.ips.index(first),
                self.ips.index(second),
                metric
            )
        )

    def get_by_ips(self, first: str, second: str) -> Optional[NetworkConnection]:
        index_of_first = self.ips.index(first)
        index_of_second = self.ips.index(second)

        for connection in self.connections:
            if connection.first == index_of_first and connection.second == index_of_second:
                return connection
            if connection.second == index_of_first and connection.first == index_of_second:
                return connection
        return None

    # TODO: Optimise two methods below
    def get_adjacency_matrix(self) -> List[List[int]]:
        matrix: List[List[int]] = []
        for ip in self.ips:
            list_to_add: List[int] = []
            for ip2 in self.ips:
                if self.get_by_ips(ip, ip2) is not None:
                    list_to_add.append(1)
                else:
                    list_to_add.append(0)
            matrix.append(list_to_add)
        return matrix

    def get_metrics_matrix(self) -> List[List[int]]:
        matrix: List[List[int]] = []
        for ip in self.ips:
            list_to_add: List[int] = []
            for ip2 in self.ips:
                el: Optional[NetworkConnection] = self.get_by_ips(ip, ip2)
                if el is None:
                    list_to_add.append(0)
                else:
                    list_to_add.append(el.metric)
            matrix.append(list_to_add)
        return matrix
