#include <stdio.h>
#include <string.h>

int linhas, colunas;

// Direções: 8 conectividades (vertical, horizontal, diagonal)
int dx[8] = {-1, -1, -1, 0, 0, 1, 1, 1};
int dy[8] = {-1, 0, 1, -1, 1, -1, 0, 1};

// DFS recursiva para contar o tamanho da colónia
int dfs(int x, int y, char matriz[100][100], int visitado[100][100]) {
    if (x < 0 || x >= linhas || y < 0 || y >= colunas) return 0;
    if (matriz[x][y] != '#' || visitado[x][y]) return 0;

    visitado[x][y] = 1;
    int tamanho = 1;

    for (int i = 0; i < 8; i++) {
        int nx = x + dx[i];
        int ny = y + dy[i];
        tamanho += dfs(nx, ny, matriz, visitado);
    }

    return tamanho;
}

int main() {
    int a;
    scanf("%d", &a);

    for (int i = 0; i < a; i++) {
        scanf("%d %d", &linhas, &colunas);

        char matriz[linhas][100];
        int visitado[100][100] = {0};  // zera tudo

        for (int j = 0; j < linhas; j++) {
            scanf("%s", matriz[j]); // ler linha completa
        }

        int maior_colonia = 0;

        for (int j = 0; j < linhas; j++) {
            for (int k = 0; k < colunas; k++) {
                if (matriz[j][k] == '#' && !visitado[j][k]) {
                    int tamanho = dfs(j, k, matriz, visitado);
                    if (tamanho > maior_colonia) {
                        maior_colonia = tamanho;
                    }
                }
            }
        }

        printf("%d\n", maior_colonia);
    }

    return 0;
}
