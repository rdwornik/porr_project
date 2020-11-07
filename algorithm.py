import numpy as np
import copy
###Static variables###
alfa = 1
beta = 1
rho = 0.5
#Liczba mrówek
M = 6
#Wartość początkowa
tau_0 = 1
#Inicjalizacja algorytmu
G = [[1,1],[1,1]]
#Metryka
Metric = [[5,4],[3,2]]
#liczba kolumn
D = len(G[0])
#liczba wierszy
R = len(G)
#Tetha inizjalizacja
tau = np.zeros((R,D))
tau[...] = [tau_0]
tau_all = [copy.deepcopy(tau) for i in range(0,M)] 
tau_best = np.zeros((1,D))
#Liczba cykli
c = 1
#Wartość Je
Je = np.zeros((R,D))
#Wartość Je best
Je_best = np.zeros((1,D))

#funkcja celu
def goal_function(j,i):
    Je[j][i]=Metric[j][i]
    return Je[j][i]

def delta_tau_k_ij(t,k,j,i):
    if(G[j][i]):
        tau_all[k][j][i]=1/goal_function(j,i)
    else:
        tau_all[k][j][i]=0

def delta_tau_best_ij(j,i):
    if(Je[j][i] > Je_best[0][i]):
        Je_best[0][i] = Je[j][i] 
        tau_best[0][i] = 1/Je_best[0][i]
    
def tau_ij(t,j,i):
    return tau[j][i]
#TODO do wymyślenia funkcja heurystyczna
def eta_ij(t,j,i):
    return Metric[j][i]

#TODO pytanie czy zapamiętujemy wartość tablicy feromonów po każdej iteracji
def tau_ij(t,i,j):
    def tau_func(k):
        return tau_all[k][j][i] 
    tau[j][i] = (1-rho)*tau[j][i] + new_sum(M,tau_func) + rho*tau_best[0][j]

def new_sum(N, fun):
    sum = 0
    for i in range(0,N):
        sum += fun(i)
    return sum

'''
Probability of selecting node 'j' for ant 
being currently in node 'i'
'''
def p_ij(t,i,j):
    pass

