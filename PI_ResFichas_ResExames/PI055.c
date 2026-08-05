#include <stdio.h>

int dx[4] = {-1,0,0,1};
int dy[4] = {0,1,-1,0};

int dfs(int x, int y, int visitados[100][100], char matriz[100][100], int linhas, int colunas) {

    if (x < 0 || x >= linhas || y < 0 || y >= colunas) return 0;
    if (matriz[x][y] != '.' || visitados[x][y]) return 0;

    visitados[x][y]=1;
    int lagos = 0;
    lagos = 1;


    for (int i = 0; i < 4; i++) {
        int nx = x + dx[i];
        int ny = y + dy[i];

        lagos += dfs(nx,ny, visitados, matriz, linhas, colunas);
    }
    return lagos;
}



int main() {

    int linhas = 0;
    scanf("%d",&linhas);

    int colunas = 0;
    scanf("%d",&colunas);

    char matriz [100][100];


    for (int i = 0; i < linhas; i++) {
        for (int j = 0; j < colunas; j++) {
            scanf(" %c", &matriz[i][j]);
        }
    }

    int total = 0;
    int visitados[100][100] = {0};

    for (int i = 0; i < linhas; i++) {
        for (int j = 0; j < colunas; j++) {
            if (matriz[i][j] == '.' && !visitados[i][j]) {
                dfs(i,j,visitados,matriz,linhas,colunas);
                total ++;
            }
        }
    }

    printf("%d\n", total);

    return 0;
}