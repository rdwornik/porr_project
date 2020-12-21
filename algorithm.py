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
#Liczba mrowek
M = 10
#Wartość początkowa
tau_0 = 0.1

#WAŻNE !!! jeśli w grafie nie ma połączenie i jest 0 to w metryce też musi być 0
#Ustalenie istniejących ścieżek w grafie
G = [[1,0,1],\
     [1,1,1],\
     [0,1,1]]
#Metryka
Metric = [[5,0,3],\
          [3,2,1],\
          [0,2,1]]

###NIE EDYTUJEMY KOLEJNYCH PARAMETRÓW###
#liczba kolumn
D = len(G[0])
#liczba wierszy
R = len(G)
#tau inizjalizacja
tau = zeros((R,D))
tau[...] = [tau_0]
#tau k inizjalizacja
tau_all = [copy.deepcopy(tau) for i in range(0,M)]
#tau best inizjalizacja
tau_best = zeros((R,D))
#Wartość Je_best best przechowuje [t,Je_best] t kolejna iteracja a Je_best to wartość funkcji celu
Je_best = [(0,0)]  

#definicja funkcji celu na chwilę obecną równomiernie rozprowadza feromony na węzły które należą do najlepszej ścieżki
def goal_function(K):
    sum = 0
    for j, i in K:
        if G[j][i] and Metric[j][i]:
            sum += Metric[j][i]
        else:
            return 0
    #rówżnomiernie rozprowadzamy wartość funkcji celu na poszczególny węzeł
    Je = sum/D
    return Je

#TODO do wymyślenia funkcja heurystyczna na chwilę obecną zwraca wartość metryki
def get_eta_ij(t,j,i):
        return Metric[j][i]
def set_delta_tau_k_ij(t,k,K,Je):
    for j, i in K:
        if G[j][i] and Je:
            tau_all[k][j][i] = 1/Je
        else:
            tau_all[k][j][i] = 0

def set_delta_tau_best_ij(t,K,Je):
    if Je_best[-1][1] == 0 or Je_best[-1][1] > Je:
        Je_best.append((t,Je))
        tau_best = zeros((R,D))
        for j, i in K:
            tau_best[j][i] = Je
    else:
        Je_best.append((t,Je_best[-1][1]))
        
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

def run_aco_algorithm():
    elements = [e for e in range(0,R)]
    #ilość cykli
    for t in range(1, C+1):
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
            Je = goal_function(K)
            #Pozostawienie feromonu po przejściu pierwszej ścieżki
            set_delta_tau_k_ij(t,k,K,Je)
            #sprawdzamy czy najlepsza ścieżka do tej pory
            set_delta_tau_best_ij(t,K,Je)
        #ustawiamy tablice feromonuów
        for i in range(0,D):
            for j in range(0,R):
                set_tau_ij(t,j,i) 

#usunięcie duplikatu w tuplach i posortowanie względem iteracji
def removeDuplicates(lst):   
    return sorted([t for t in (set(tuple(i) for i in lst))], key=lambda tup : tup[0])

#implementacja algorytmu ruletki
def roulette_selection(elements, weights):
    return choice(elements, p=weights)
    
#funckja sumy zamiast sigmy
def new_sum(N, fun):
    sum = 0
    for i in range(0,N):
        sum += fun(i)
    return sum

if __name__ == "__main__":
    run_aco_algorithm()
    #print tablicy feromonów
    print(tau)
    print(removeDuplicates(Je_best))