#include <stdio.h>

int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

void dfs(int x, int y, char mapa[1000][1000], int visitado[1000][1000], int n, int m) {
    if (x < 0 || x >= n || y < 0 || y >= m) return;
    if (mapa[x][y] != '#' || visitado[x][y]) return;

    visitado[x][y] = 1;

    for (int i = 0; i < 4; i++) {
        int nx = x + dx[i];
        int ny = y + dy[i];
        dfs(nx, ny, mapa, visitado, n, m);
    }
}

int contar_lagos(int n, int m, char mapa[n][m]) {
    int visitado[1000][1000] = {0};
    int total = 0;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (mapa[i][j] == '#' && !visitado[i][j]) {
                dfs(i, j, mapa, visitado, n, m);
                total++;
            }
        }
    }

    return total;
}

void mudancas(int n, int m, char mapa[n][m], char sentido, int aonde) {
    aonde--;

    if (sentido == 'R') {
        for (int j = 0; j < m; j++) {
            if (mapa[aonde][j] == '#') {
                mapa[aonde][j] = '.';
            }
        }
    }

    if (sentido == 'C') {
        for (int i = 0; i < n; i++) {
            if (mapa[i][aonde] == '#') {
                mapa[i][aonde] = '.';
            }
        }
    }
}

int main() {
    int n, m;
    scanf("%d %d", &n, &m);

    char mapa[n][m];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            scanf(" %c", &mapa[i][j]);
        }
    }

    int a;
    scanf("%d", &a);

    char sentido[a];
    int sitio[a];

    for (int i = 0; i < a; i++) {
        scanf(" %c %d", &sentido[i], &sitio[i]);
    }

    int lagos = contar_lagos(n, m, mapa);
    printf("%d\n", lagos);

    for (int i = 0; i < a; i++) {
        mudancas(n, m, mapa, sentido[i], sitio[i]);
        lagos = contar_lagos(n, m, mapa);
        printf("%d\n", lagos);
    }

    return 0;
}

