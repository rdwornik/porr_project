from numpy.random import choice

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