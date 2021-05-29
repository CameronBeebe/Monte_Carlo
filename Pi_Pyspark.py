import pyspark
import numpy as np
import argparse

num_points = 1000
num_processes = 4


parser = argparse.ArgumentParser()
parser.add_argument("--points", "-pts", type=int, help="The number of points for a process to simulate in a parallelized Monte Carlo estimation of pi.")
parser.add_argument("--processes", "-procs", type=int, help="The number of processes to initialize the SparkContext with.") 
args = parser.parse_args()

if args.points:
    #print("printing...",args.points)
    num_points = args.points

if args.processes:
    num_processes = args.processes



# Take processes from command line parser.
sc = pyspark.SparkContext('local[{}]'.format(num_processes))
tc = pyspark.TaskContext()

print('default parallelism: {}'.format(sc.defaultParallelism))

# RDD will be partitioned according to sc.defaultParallelism
num_ranks = sc.defaultParallelism


def generate_points(num_pairs):
    print('generating points...')
    return np.random.uniform(high=1, size=(num_pairs,2))


# Multiply the number of points by number of ranks (cores) for RDD of points.
points = sc.parallelize(generate_points(num_ranks * num_points))

num_partitions = points.getNumPartitions()

print('Check number of partitions are equal to the default parallelization (number of cores): {} == {}, {}'.format(num_partitions, num_ranks, num_partitions == num_ranks))

# print(points.take(1))

# The main change from the MPI script (for now) is that the calc_lengths function must operate on a RDD object.
# This can probably be improved to a generator, but the simple data works fine this way.
# The rest of the code is the same as the MPI example.
def calc_lengths(pair_RDD):
    return np.array([np.linalg.norm(i) for i in pair_RDD.collect()])

lengths = calc_lengths(points)

def ratio(lengths):
    count = len(np.where(lengths < 1)[0])
    #print(count)
    return count / len(lengths)

inv = ratio(lengths)

pi_estimate = inv*4

how_close = np.abs(np.pi - pi_estimate)

print("pi estimate:", pi_estimate, "with closeness:", how_close, "on a ratio calculated by the number of lengths", len(lengths))

sc.stop()