alfa = 1
beta = 1
rho = 0.5
#Liczba cykli
C = 20
#Liczba mrowek
M = 10
#Wartość początkowa
tau_0 = 0.1

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

#WAŻNE !!! jeśli w grafie nie ma połączenie i jest 0 to w metryce też musi być 0
#Ustalenie istniejących ścieżek w grafie

with open('input_G.txt', 'r') as f:
    G = [[int(num) for num in line.split(',')] for line in f]

G2 = np.array(G)
n = np.count_nonzero(G2)
A = np.zeros((n+2,n+2))

rows1 = np.where(G2[:,0] == 1)[0]
for i in rows1:
    A[i+1][0] = 1

c1 = len(rows1) + 1
c2 = 1
for col in np.transpose(G)[1:]:
    rows2 = np.where(col == 1)[0]
    if len(rows1):
        for j in rows1:
            tmp = c1
            for i in rows2:
                i1 = c1
                j1 = c2
                A[i1][j1] = 1
                c1+=1
            c2+=1
            c1 = tmp
    else:
        c2+=1
    rows1 = rows2
    c1+=len(rows1)

rows1 = np.where(G2[:,-1] == 1)[0]
for i in rows1:
    A[-1][c2] = 1
    c2+=1   


G3 = A + np.transpose(A)
G4 = nx.from_numpy_matrix(np.array(G3))  
# nx.draw(G4, with_labels=True) 
f = plt.figure()
nx.draw(G4, with_labels=True, ax=f.add_subplot(111))
f.savefig("graph.png")

with open('input_M.txt', 'r') as f:
    Metric = [[int(num) for num in line.split(',')] for line in f]


G2 = np.array(Metric)
n = np.count_nonzero(G2)
A = np.zeros((n+2,n+2))


rows1 = np.where(G2[:,0] != 0)[0]
for i in rows1:
    A[i+1][0] = Metric[i][0]

c1 = len(rows1) + 1
c2 = 1
for idx, col in enumerate(np.transpose(Metric)[1:],1):
    rows2 = np.where(col != 0)[0]
    if len(rows1):
        for j in rows1:
            tmp = c1
            for i in rows2:
                i1 = c1
                j1 = c2
                A[i1][j1] = Metric[i][idx]
                c1+=1
            c2+=1
            c1 = tmp
    else:
        c2+=1
    rows1 = rows2
    c1+=len(rows1)

rows1 = np.where(G2[:,-1] != 0)[0]

for i in rows1:
    A[-1][c2] = 1
    c2+=1   

G3 = A + np.transpose(A)
G4 = nx.from_numpy_matrix(G3,create_using=nx.DiGraph) 
# G5 = nx.from_numpy_matrix(G3,create_using=nx.DiGraph) 
layout = nx.spring_layout(G4,weight=None)
# nx.draw(G4, with_labels=True) 
f = plt.figure()
labels = nx.get_edge_attributes(G4, "weight")
nx.draw(G4, pos=layout, with_labels=True, ax=f.add_subplot(111))
nx.draw_networkx_edge_labels(G4, pos=layout,edge_labels=labels)
f.savefig("graph2.png")