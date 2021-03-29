import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD

def generate_points(num_pairs):
    return np.random.uniform(high=1, size=(num_pairs,2))

points = generate_points(10000)

def calc_lengths(pairs):
    return np.array([np.linalg.norm(i) for i in pairs])

lengths = calc_lengths(points)

def ratio(lengths):
    count = len(np.where(lengths < 1)[0])
    #print(count)
    return count / len(lengths)

inv = ratio(lengths)

pi_estimate = inv*4

print("Rank: ", comm.Get_rank(), "pi estimate:", pi_estimate)
