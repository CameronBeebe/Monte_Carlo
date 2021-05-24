This is a short reference example for a common parallelization exercise using MPI.  It is a Monte Carlo estimation of Pi.

Pi_MPI.py can be run on the command line in the environment outlined in mpi_min.yaml using commands of the form "mpirun -n 4 python Pi_MPI.py -pts 1000".

TO DO:

1.  Implement the same algorithm and functionality with pyspark.  (Figure out how to have ranks/workers spit out confirmations of local work being done)

2.  Compare.
