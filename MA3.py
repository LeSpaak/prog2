""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import numpy as np
import functools
from numba import njit
import multiprocessing as mp

# Exc1
def approximate_pi(n):
    # n is the number of points
    print(f"This is the number of points: {n}")
    xblulst = []
    yblulst = []
    xredlst = []
    yredlst = []
    for _ in range(n): #Kan nog vara lst comprehension istället.
         x,y = random.uniform(-1,1),random.uniform(-1,1)

         if x**2+y**2 <= 1:
             xredlst.append(x)
             yredlst.append(y)
         else:
              xblulst.append(x)
              yblulst.append(y)

    blulst = list(zip(xblulst,yblulst)) #Onödigt. 
    redlst = list(zip(xredlst,yredlst)) #Kan använda filter funktionen för att få blue list och red lst. 
    #Kan också använda gamma funktion. Ska prova på nästa uppgift.

    approx_pi = 4 * len(redlst) / (len(redlst)+len(blulst))
    print(f"This is the approx pi: {approx_pi}")
 
    plt.scatter(xblulst,yblulst, color = 'blue')
    plt.scatter(xredlst,yredlst, color='red')
    plt.show()
    return approx_pi

# Exc2, approximation
def sphere_volume(n, d): 
    # n is the number of points
    all_lst = [[random.uniform(-1,1) for _ in range(d)] for _ in range(n)]
    # d is the number of dimensions of the sphere 
    f = lambda point :sum(list(map(lambda x : x**2, point))) <= 1
    red_lst = list(filter(f , all_lst) )
    return len(red_lst)/len(all_lst) * 2**d

#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points
    # d is the number of dimensions of the sphere 
    return np.pi**(d/2) / m.gamma(d/2+1)

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    # n is the number of points
    all_lst = [[random.uniform(-1,1) for _ in range(d)] for _ in range(n)]
    # d is the number of dimensions of the sphere 
    f = lambda point :sum(list(map(lambda x : x**2, point))) <= 1
    red_lst = list(filter(f , all_lst) )
    return len(red_lst)/len(all_lst) * 2**d
    #np is the number of processes

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    processes = []
    for _ in range(np):
        p = mp.Process(target=sphere_volume, args=[n,d])
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    return 
    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    # Exc2
    n = 100000
    d = 2
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    sphere_volume(n, d)
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11
    for _ in range(3):
        start = pc()
        sphere_volume(n, d)
        stop = pc()
        print(f"Exc3: Sequential time of {d} and {n}: {stop-start} iteration {_+1}")
    print("What is numba time?")

    for _ in range(3):
        start = pc()
        sphere_volume_numba(n, d)
        stop = pc()
        print(f"Exc3: Numba time of {d} and {n}: {stop-start} iteration {_+1}")

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    start = pc()
    sphere_volume_parallel(n, d)
    stop = pc()
    print(f"Exc4: Parallell time of {d} and {n}: {stop-start}")
    
    

if __name__ == '__main__':
	main()
