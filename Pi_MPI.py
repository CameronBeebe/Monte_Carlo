import numpy as np
import argparse
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

parser = argparse.ArgumentParser()
parser.add_argument("--points", "-pts", type=int, help="The number of points for a process to simulate in a parallelized Monte Carlo estimation of pi.")
args = parser.parse_args()

num_points = 1000

if args.points:
    #print("printing...",args.points)
    num_points = args.points

def generate_points(num_pairs):
    return np.random.uniform(high=1, size=(num_pairs,2))

points = generate_points(num_points)

def calc_lengths(pairs):
    return np.array([np.linalg.norm(i) for i in pairs])

lengths = calc_lengths(points)

def ratio(lengths):
    count = len(np.where(lengths < 1)[0])
    #print(count)
    return count / len(lengths)

def comm_length_data(lengths):
    new_lengths = comm.gather(lengths, root=0)
    if rank == 0:
        print("root rank", rank, "gathering lengths from other ranks")
        lengths = np.concatenate(new_lengths,axis=0)
    else:
        print("non-root rank", rank, "leaving lengths alone")
        lengths = lengths
        #print("rank 0 new_lengths size", new_lengths.size)
        #print("rank 0 new_lengths", new_lengths)
    return lengths


gathered_lengths = comm_length_data(lengths)

lengths = gathered_lengths

inv = ratio(lengths)

pi_estimate = inv*4

how_close = np.abs(np.pi - pi_estimate)

print("Rank: ", comm.Get_rank(), "pi estimate:", pi_estimate, "with closeness:", how_close, "on a ratio calculated by the number of lengths", len(lengths))
