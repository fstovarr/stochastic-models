/**
 * Simulación del problema de percolación
 * Autor: Fabio Steven Tovar Ramos
 * Compilación g++: g++ percolacion.cpp -o percolacion -fopenmp -pthread
 * 
 * Ejecución:
 * ./percolacion num_rocas M N hilos (delta_p)
 * 
 * Ejemplo:
 * ./percolacion 10000 5 5 16
 * 
 * ./percolacion 10000 5 5 16 0.1
 * 
 * */

#include <omp.h>
#include <iostream>
#include <cstdlib>
#include <random>
#include <string.h>
#include <queue>
#include <utility>

using namespace std;

// PAD para evitar false sharing en el paralelismo
#define PAD 8

// Función para limpiar la cola
void clear(queue<pair<int, int>> &q) {
   queue<pair<int, int>> empty;
   swap(q, empty);
}

// Función que dado un vector de booleanos de dos dimensiones y los posibles movimientos que se puedan realizar,
// indica si hay un camino que une la parte superior con la inferior.
// En el vector, true indica que es un espacio lleno, y false que hay una porosidad
// m y n son las dimensiones del vector
bool find_path(int m, int n, bool **rock, int possible_moves[][2]) {
    int void_top = n, void_bottom = n;

    for (int i = 0; i < n; i++) {
        void_top -= rock[0][i];
        void_bottom -= rock[m - 1][i];
    }

    if(void_top == 0 || void_bottom == 0) return false;

    int count = min(void_top, void_bottom);
    bool top = void_top == count;

    bool visited[count][m][n];
    memset(visited, false, count * m * n * sizeof(bool));
    
    queue<pair<int, int>> to_visit;

    pair<int, int> current;
    int c_x = 0, c_y = 0, goal = top ? (m - 1) : 0, start = top ? 0 : (m - 1);

    // BFS
    for (int i = 0, c = 0; i < m && c < count; i++) {
        if(rock[start][i] == true) continue;
        
        to_visit.push(make_pair(start, i));
        visited[c][start][i] = true;

        while(to_visit.size() > 0) {
            current = to_visit.front();
            to_visit.pop();

            if(current.first == goal)
                return true;

            for (int j = 0; j < 4; j++) {
                c_y = current.first + possible_moves[j][0];
                c_x = current.second + possible_moves[j][1];
                if (c_x < n && c_x >= 0 && c_y < m && c_y >= 0 && !visited[c][c_y][c_x] && rock[c_y][c_x] == false) {
                    // printf("(%d, %d)\n", c_y, c_x);
                    to_visit.push(make_pair(c_y, c_x));
                    visited[c][c_y][c_x] = true;
                }
            }
        }
        c++;
        clear(to_visit);
    }

    return false;
}

// Funcion que simula la creación de una roca dado un threshold, que es en este caso
// la probabilidad por la cual se itera, y la retorna en la variable rock.
void simulate_rock(int m, int n, double threshold, int seed, bool **rock) {
    double u = 0.0;

    mt19937 gen(seed);
    uniform_real_distribution<> dis(0, 1);

    // simulate rock
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            u = dis(gen);
            rock[i][j] = (u > threshold);
            // printf("%d ", rock[i][j]);
        }
        // cout << endl;
    }
}

int main(int argc, char *argv[]) {
    if(argc < 5) {
        printf("Wrong arguments!\n");
        return -1;
    }

    int ROCKS_PER_SIMULATION;
    sscanf(argv[1], "%d", &ROCKS_PER_SIMULATION);

    int M;
    sscanf(argv[2], "%d", &M);

    int N;
    sscanf(argv[3], "%d", &N);

    int THREADS;
    sscanf(argv[4], "%d", &THREADS);

    double DELTA_P = 0.001;
    if(argv[5] != NULL) sscanf(argv[5], "%lf", &DELTA_P);

    string name = "results_" + to_string(M) + "_" + to_string(N) + ".csv";

    freopen(name.c_str(), "w", stdout);

    int iterations = (1 / DELTA_P);

    // Vector de resultados con un PAD para evitar false sharing
    double results[iterations * PAD];

    // Posiciones a las cuales se puede llegar dada una coordenada
    int possible_moves[][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    printf("p, theta_p\n");

    bool **rock[THREADS];

    // Vectores que contendrán cada una de las rocas simuladas,
    // uno globalmente por cada hilo para evitar memory leaks
    for (int i = 0; i < THREADS; i++) {
        rock[i] = new bool *[M];
        for (int k = 0; k < M; k++)
            for (int j = 0; j < N; j++)
                rock[i][k] = new bool[N];
    }

    #pragma omp parallel for schedule (guided) num_threads(THREADS)
    for (int p = 0; p < iterations; p++) {
        double total = 0;
        int id = omp_get_thread_num();

        // Simulación de ROCKS_PER_SIMULATION rocas para un valor de p específico
        for (int i = 0; i < ROCKS_PER_SIMULATION; i++) {
            simulate_rock(M, N, p * 1.0 * DELTA_P, i, rock[id]);
            total += find_path(M, N, rock[id], possible_moves);
        }

        results[p * PAD] = total;
    }

    // Volcado de resultados al csv
    for (int i = 0; i < iterations; i++)
        printf("%f, %f\n", DELTA_P * i, results[i * PAD] / ROCKS_PER_SIMULATION);
}