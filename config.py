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

G = [[1,1,0],\
     [1,1,1],\
     [0,1,1]]
     
#Metryka
Metric = [[5,1,0],\
          [3,2,1],\
          [0,2,4]]
