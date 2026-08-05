#include <stdio.h>

int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

int dfs(int x, int y, char matriz[100][100], int visitados[100][100], int linhas, int colunas,int encontrado) {
    if (x < 0 || x >= linhas || y < 0 || y >= colunas) return 0;
    if (matriz[x][y] == '#' || visitados[x][y]) return 0;

    visitados[x][y] = 1;

    int total = 0;
    if (matriz[x][y] == 'P') {
        total ++;
        return total;
    }

    for (int i = 0; i < 4; i++) {
        int nx = x + dx[i];
        int ny = y + dy[i];
        total +=dfs(nx, ny, matriz, visitados, linhas, colunas, encontrado);
    }
    return total;
}

int main() {

    int a = 0;
    scanf("%d", &a);

    for (int i = 0; i < a; i++) {
        int linhas = 0;
        scanf("%d", &linhas);

        int colunas = 0;
        scanf("%d", &colunas);

        char matriz [100][100];
        int visitados [100][100] = {0};
        int x = 0;
        int y = 0;

        for (int j = 0; j < linhas; j++) {
            for (int k = 0; k < colunas; k++) {
                scanf(" %c", &matriz[j][k]);
                if (matriz[j][k] == 'J') {
                    x = j;
                    y = k;
                }
            }
        }
        int encontrado = 0;
        encontrado += dfs(x, y, matriz, visitados, linhas, colunas,encontrado);
        if (encontrado == 1) {
            printf("yes\n");
        } else {
            printf("no\n");
        }
    }
    return 0;
}