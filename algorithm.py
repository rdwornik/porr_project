import copy
from typing import List

from numpy import zeros
from numpy.random import choice


class EditableParams:
    def __init__(self,
                 alfa: float,
                 beta: float,
                 rho: float,
                 C: int,
                 M: int,
                 tau_0: float
                 ):
        self.alfa = alfa
        self.beta = beta
        self.rho = rho

        # Liczba cykli
        self.C = C

        # Liczba mrowek
        self.M = M

        # Wartość początkowa
        self.tau_0 = tau_0


class Calculator:
    def __init__(self,
                 editable_params: EditableParams,
                 G: List[List[float]],
                 Metric: List[List[float]],
                 ):
        self.editable_params = editable_params

        # WAŻNE !!! jeśli w grafie nie ma połączenie i jest 0 to w metryce też musi być 0
        self.G = G
        self.Metric = Metric

        # liczba kolumn
        self.D = len(G[0])

        # liczba wierszy
        self.R = len(G)

        # tau inicjalizacja
        self.tau = zeros((self.R, self.D))
        self.tau[...] = [self.editable_params.tau_0]

        # tau k inizjalizacja
        self.tau_all = [copy.deepcopy(self.tau) for i in range(0, self.editable_params.M)]

        # tau best inizjalizacja
        self.tau_best = zeros((self.R, self.D))

        # Wartość Je_best best przechowuje [t,Je_best] t kolejna iteracja a Je_best to wartość funkcji celu
        self.Je_best = [(0, 0)]

    # definicja funkcji celu na chwilę obecną równomiernie rozprowadza feromony na węzły które należą do najlepszej ścieżki
    def goal_function(self, K):
        sum = 0
        for j, i in K:
            if self.G[j][i] and self.Metric[j][i]:
                sum += self.Metric[j][i]
            else:
                return 0
        # rówżnomiernie rozprowadzamy wartość funkcji celu na poszczególny węzeł
        return sum / self.D

    # TODO do wymyślenia funkcja heurystyczna na chwilę obecną zwraca wartość metryki
    def get_eta_ij(self, t, j, i):
        return self.Metric[j][i]

    def set_delta_tau_k_ij(self, t, k, K, Je):
        for j, i in K:
            if self.G[j][i] and Je:
                self.tau_all[k][j][i] = 1 / Je
            else:
                self.tau_all[k][j][i] = 0

    def set_delta_tau_best_ij(self, t, K, Je):
        if self.Je_best[-1][1] == 0 or self.Je_best[-1][1] > Je:
            self.Je_best.append((t, Je))
            tau_best = zeros((self.R, self.D))
            for j, i in K:
                tau_best[j][i] = Je
        else:
            self.Je_best.append((t, self.Je_best[-1][1]))

    # TODO pytanie czy zapamiętujemy wartość tablicy feromonów po każdej iteracji
    def set_tau_ij(self, t, j, i):
        def tau_func(k):
            return self.tau_all[k][j][i]

        self.tau[j][i] = (1 - self.editable_params.rho) * self.tau[j][i] + self.new_sum(self.editable_params.M,
                                                                                        tau_func) + self.editable_params.rho * \
                         self.tau_best[j][i]

    # Prawdopodobieństwo wybrania węzła j będąc na węźle i
    def get_p_k_ij(self, t, k, j, i):
        def tau_func(x):
            return pow(self.tau[x][i], self.editable_params.alfa) * pow(self.get_eta_ij(t, x, i),
                                                                        self.editable_params.beta)

        return pow(self.tau[j][i], self.editable_params.alfa) * pow(self.get_eta_ij(t, j, i),
                                                                    self.editable_params.beta) / self.new_sum(self.R,
                                                                                                              tau_func)

    def run_aco_algorithm(self):
        elements = [e for e in range(0, self.R)]
        # ilość cykli
        for t in range(1, self.editable_params.C + 1):
            # ilość mrówek
            for k in range(0, self.editable_params.M):
                # losowanie ścieżek
                K = []
                for i in range(0, self.D):
                    weights = []
                    for j in range(0, self.R):
                        weights.append(self.get_p_k_ij(t, k, j, i))
                    j = self.roulette_selection(elements, weights)
                    K.append((j, i))
                Je = self.goal_function(K)
                # Pozostawienie feromonu po przejściu pierwszej ścieżki
                self.set_delta_tau_k_ij(t, k, K, Je)
                # sprawdzamy czy najlepsza ścieżka do tej pory
                self.set_delta_tau_best_ij(t, K, Je)
            # ustawiamy tablice feromonuów
            for i in range(0, self.D):
                for j in range(0, self.R):
                    self.set_tau_ij(t, j, i)

    # usunięcie duplikatu w tuplach i posortowanie względem iteracji
    def removeDuplicates(self, lst):
        return sorted([t for t in (set(tuple(i) for i in lst))], key=lambda tup: tup[0])

    # implementacja algorytmu ruletki
    def roulette_selection(self, elements, weights):
        return choice(elements, p=weights)

    # funckja sumy zamiast sigmy
    def new_sum(self, N, fun):
        sum = 0
        for i in range(0, N):
            sum += fun(i)
        return sum

    def printInfo(self):
        print(self.tau)
        print(self.removeDuplicates(self.Je_best))