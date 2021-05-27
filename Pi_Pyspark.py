import pyspark
import numpy as np
import argparse

sc = pyspark.SparkContext('local[*]')

parser = argparse.ArgumentParser()
parser.add_argument("--points", "-pts", type=int, help="The number of points for a process to simulate in a parallelized Monte Carlo estimation of pi.")
args = parser.parse_args()

num_points = 1000

if args.points:
    #print("printing...",args.points)
    num_points = args.points
    

def generate_points(num_pairs):
    return np.random.uniform(high=1, size=(num_pairs,2))

points = sc.parallelize(generate_points(num_points))

print(points.take(1))

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
