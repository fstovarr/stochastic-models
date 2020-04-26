# !/bin/bash

g++ percolacion.cpp -o percolacion -fopenmp -pthread

echo "Running (5, 5)"
./percolacion 10000 5 5 16
echo "Running (2, 100)"
./percolacion 10000 2 100 16
echo "Running (100, 2)"
./percolacion 10000 100 2 16
echo "Running (30, 70)"
./percolacion 10000 30 70 16
echo "Running (70, 30)"
./percolacion 10000 70 30 16
echo "Running (200, 200)"
./percolacion 10000 200 200 16