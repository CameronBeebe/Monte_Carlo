This is a short reference example for a common parallelization exercise.  It is a Monte Carlo estimation of Pi.  One implementation is in MPI, the other is in Pyspark to compare.

Code is not optimal, but tries to be clear and demonstrative (can be improved still).

Pi_MPI.py can be run on the command line in the environment outlined in mpi_min.yaml using commands of the form "mpirun -n 4 python Pi_MPI.py -pts 1000".

Pi_Pyspark.py can be run on the command line using commands of the form "python Pi_Pyspark.py -pts 1000".

TO DO:

1.  Figure out how to have Pyspark ranks/workers spit out confirmations of local work being done like in MPI.

2.  Compare.
