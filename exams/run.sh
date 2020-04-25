# !/bin/bash

g++ percolacion.cpp -o percolacion -fopenmp -pthread

echo "Running (2, 100)"
./percolacion 10000 2 100

# echo "Running (100, 2)"
# ./percolacion 10000 100 2
# echo "Running (30, 70)"
# ./percolacion 10000 30 70
# echo "Running (70, 30)"
# ./percolacion 10000 70 30
# echo "Running (200, 200)"
# ./percolacion 10000 200 200