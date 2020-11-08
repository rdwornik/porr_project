import numpy as np
import copy
from numpy.random import choice
from numpy import zeros

###Static variables###
###PARAMETRY DO EDYCJI###
alfa = 1
beta = 1
rho = 0.5
#Liczba cykli
C = 20
#Liczba mrówek
M = 10
#Wartość początkowa
tau_0 = 1
#Inicjalizacja algorytmu
G = [[1,1,1],\
    [1,1,1],\
    [1,1,1]
    ]
#Metryka
Metric = [[5,1000,3],[3,2,1],[3,2,1]]

###NIE EDYTUJEMY PARAMETRÓW###
#liczba kolumn
D = len(G[0])
#liczba wierszy
R = len(G)
#Tetha inizjalizacja
tau = zeros((R,D))
tau[...] = [tau_0]
tau_all = [copy.deepcopy(tau) for i in range(0,M)] 
tau_best = zeros((R,D))
#Lista Je przechowuje tuple (t,Je) gdzie t to iteracja Je to wartość funckji celu w danej iteracji
Je = []
#Wartość Je_best best przechowuje [K,Je_best] gzie K to lista przechwoująca węzły ścieżki a Je Best to wartość funkcji celu
Je_best = [0]  


def goal_function(K):
    sum = 0
    for j, i in K:
        sum += Metric[j][i]
    #rówżnomiernie rozprowadzamy wartość funkcji celu na poszczególny węzeł
    Je = sum/D
    return Je

def set_delta_tau_k_ij(t,k,K,Je):
    for j, i in K:
        if G[j][i]:
            tau_all[k][j][i] = 1/Je
        else:
            tau_all[k][j][i] = 0

def set_delta_tau_best_ij(K,Je):
        Je_best[0] = Je
        tau_best = zeros((R,D))
        for j, i in K:
            tau_best[j][i] = Je
        
#TODO do wymyślenia funkcja heurystyczna
def get_eta_ij(t,j,i):
        return Metric[j][i]

#TODO pytanie czy zapamiętujemy wartość tablicy feromonów po każdej iteracji
def set_tau_ij(t,j,i):
    def tau_func(k):
        return tau_all[k][j][i] 
    tau[j][i] = (1-rho)*tau[j][i] + new_sum(M,tau_func) + rho*tau_best[j][i]

#Prawdopodobieństwo wybrania węzła j będąc na węźle i
def get_p_k_ij(t,k,j,i):
    def tau_func(x):
        return pow(tau[x][i],alfa)*pow(get_eta_ij(t,x,i),beta)
    return pow(tau[j][i],alfa)*pow(get_eta_ij(t,j,i),beta)/new_sum(R,tau_func)

#implementacja algorytmu ruletki
def roulette_selection(elements, weights):
    return choice(elements, p=weights)
    
#funckja sumy zamiast sigmy
def new_sum(N, fun):
    sum = 0
    for i in range(0,N):
        sum += fun(i)
    return sum

def run_aco_algorithm():
    elements = [e for e in range(0,R)]
    #ilość cykli
    for t in range(0, C):
        #ilość mrówek
        for k in range(0,M):
            #losowanie ścieżek
            K = []
            for i in range(0,D):
                weights = []
                for j in range (0,R):
                    weights.append(get_p_k_ij(t,k,j,i))
                j = roulette_selection(elements,weights)
                K.append((j,i))
            je = goal_function(K)
            #Pozostawienie feromonu po przejściu pierwszej ścieżki
            set_delta_tau_k_ij(t,k,K,je)
            #sprawdzamy czy najlepsza ścieżka do tej pory
            if Je_best[0] == 0 or Je_best[0] > je:
                set_delta_tau_best_ij(K,je)
        #ustawiamy tablice feromonuów
        for i in range(0,D):
            for j in range(0,R):
                set_tau_ij(t,j,i)
        Je.append((t,je))
    return tau

if __name__ == "__main__":
    tau = run_aco_algorithm()
    #print tablicy feromonów
    print(tau)
    