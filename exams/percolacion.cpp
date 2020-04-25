// g++ percolacion.cpp -o percolacion -fopenmp -pthread

#include <iostream>
#include <cstdlib>
#include <random>
#include <string.h>
#include <queue>
#include <utility>

using namespace std;

#define DELTA_P 0.001
#define PAD 8

bool find_path(int m, int n, bool **rock) {
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
    
    queue<pair<int, int>> to_visit[count];

    int possible_moves[][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    pair<int, int> current;
    int c_x = 0, c_y = 0, goal = top ? (m - 1) : 0, start = top ? 0 : (m - 1);

    for (int i = 0, c = 0; i < m && c < count; i++) {
        if(rock[start][i] == true) continue;
        to_visit[c].push(make_pair(start, i));
        visited[c][start][i] = true;

        while(to_visit[c].size() > 0) {
            current = to_visit[c].front();
            to_visit[c].pop();

            if(current.first == goal)
                return true;

            for (int j = 0; j < 4; j++) {
                c_y = current.first + possible_moves[j][0];
                c_x = current.second + possible_moves[j][1];
                if (c_x < n && c_x >= 0 && c_y < m && c_y >= 0 && !visited[c][c_y][c_x] && rock[c_y][c_x] == false) {
                    // printf("(%d, %d)\n", c_y, c_x);
                    to_visit[c].push(make_pair(c_y, c_x));
                    visited[c][c_y][c_x] = true;
                }
            }
        }
        c++;
    }

    return false;
}

bool** simulate_rock(int m, int n, double threshold, int seed) {
    bool **rock = new bool *[m];
    double u = 0.0;

    mt19937 gen(seed);
    uniform_real_distribution<> dis(0, 1);

    // simulate rock
    for (int i = 0; i < m; i++) {
        rock[i] = new bool[n];
        for (int j = 0; j < n; j++) {
            u = dis(gen);
            rock[i][j] = (u > threshold);
            // printf("%d ", rock[i][j]);
        }
        // cout << endl;
    }

    return rock;
}

int main(int argc, char *argv[]) {
    if(argc < 3) {
        printf("Wrong arguments!\n");
        return -1;
    }

    int ROCKS_PER_SIMULATION;
    sscanf(argv[1], "%d", &ROCKS_PER_SIMULATION);

    int M;
    sscanf(argv[2], "%d", &M);

    int N;
    sscanf(argv[3], "%d", &N);

    string name = "results_" + to_string(M) + "_" + to_string(N) + ".csv";
    
    freopen(name.c_str(), "w", stdout);

    int iterations = (1 / DELTA_P);
    double results[ iterations * PAD];

    printf("p, theta_p\n");

    #pragma omp parallel for
    for (int p = 0; p < iterations; p++) {
        double total = 0;
        for (int i = 0; i < ROCKS_PER_SIMULATION; i++) {
            bool **rock = simulate_rock(M, N, p * 1.0 * DELTA_P, i);
            total += find_path(M, N, rock);
        }
        results[p * PAD] = total;
    }

    for (int i = 0; i < iterations; i++)
        printf("%f, %f\n", DELTA_P * i, results[i * PAD] / ROCKS_PER_SIMULATION);
}