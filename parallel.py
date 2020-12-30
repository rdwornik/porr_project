import numpy as np
import pymp

from utils import removeDuplicates, new_sum, roulette_selection
from config import G, Metric, alfa, beta, rho, C, M, tau_0

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx

#liczba kolumn
D = len(G[0])
#liczba wierszy
R = len(G)
#tau inizjalizacja
tau = pymp.shared.array(np.array((R,D)))
tau[...] = tau_0

#tau k inizjalizacja
tau_all = pymp.shared.array(np.array((M,R,D)))
tau_all[...] = tau_0

#tau best inizjalizacja
tau_best = pymp.shared.array(np.array((R,D)))

#Wartość Je_best best przechowuje [t,Je_best] t kolejna iteracja a Je_best to wartość funkcji celu
Je_best = pymp.shared.list([(0,0)])

#definicja funkcji celu na chwilę obecną równomiernie rozprowadza feromony na węzły które należą do najlepszej ścieżki
def goal_function(K):
    sum = 0
    for j, i in K:
        if G[j][i] and Metric[j][i]:
            sum += Metric[j][i]
        else:
            return 0
    #rówżnomiernie rozprowadzamy wartość funkcji celu na poszczególny węzeł
    return sum
    
#TODO do wymyślenia funkcja heurystyczna na chwilę obecną zwraca wartość metryki
def get_eta_ij(t,j,i):
        return Metric[j][i]

def set_delta_tau_k_ij(t,k,K,Je,p):
    # with p.lock:
    for j, i in K:
        if G[j][i] and Je:
            tau_all[k][j][i] = 1/Je
        else:
            tau_all[k][j][i] = 0

def set_delta_tau_best_ij(t,K,Je,p):
    with p.lock:
        if Je_best[-1][1] == 0 or Je_best[-1][1] > Je:
                Je_best.append((t,Je))
                tau_best[...] = .0
                for j, i in K:
                    tau_best[j][i] = Je
        else:
            Je_best.append((t,Je_best[-1][1]))
        
#TODO pytanie czy zapamiętujemy wartość tablicy feromonów po każdej iteracji
def set_tau_ij(t,j,i,p):
    def tau_func(k):
        return tau_all[k][j][i]
    with p.lock:
        tau[j][i] = (1-rho)*tau[j][i] + new_sum(M,tau_func) + rho*tau_best[j][i]

#Prawdopodobieństwo wybrania węzła j będąc na węźle i
def get_p_k_ij(t,k,j,i):
    def tau_func(x):
        return pow(tau[x][i],alfa)*pow(get_eta_ij(t,x,i),beta)
    return pow(tau[j][i],alfa)*pow(get_eta_ij(t,j,i),beta)/new_sum(R,tau_func)

def get_Je_best(Je_best):
    return removeDuplicates(Je_best)

def get_tau():
    return tau

def run_aco_algorithm():
    elements = [e for e in range(0,R)]
    #ilość cykli
    for t in range(1, C+1):
        #ilość mrówek
        with pymp.Parallel(M) as p:
            for k in p.range(0,M):
                #losowanie ścieżek
                K = []
                with p.lock:
                    for i in range(0,D):
                        weights = []
                        for j in range (0,R):
                            weights.append(get_p_k_ij(t,k,j,i))
                        j = roulette_selection(elements,weights)
                        K.append((j,i))
                Je = goal_function(K)
                #Pozostawienie feromonu po przejściu pierwszej ścieżki
                set_delta_tau_k_ij(t,k,K,Je,p)
                #sprawdzamy czy najlepsza ścieżka do tej pory
                set_delta_tau_best_ij(t,K,Je,p)
            #ustawiamy tablice feromonuów
            for i in range(0,D):
                for j in range(0,R):
                    set_tau_ij(t,j,i,p) 
        
if __name__ == "__main__":
    run_aco_algorithm()
    #print tablicy feromonów
    print(get_tau())
    print(get_Je_best(Je_best))
    Gr = nx.from_numpy_matrix(np.matrix(G), create_using=nx.DiGraph)
    layout = nx.spring_layout(Gr)
    nx.draw(Gr, layout)
    nx.draw_networkx_edge_labels(Gr, pos=layout)
    plt.show()
    plt.savefig('books_read.png')