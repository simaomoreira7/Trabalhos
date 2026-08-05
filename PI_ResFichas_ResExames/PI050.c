#include <stdio.h>

#include <stdio.h>

int dx[4] = {0, 0, 1, -1};
int dy[4] = {1, -1, 0, 0};

int main() {
    int n, m;
    scanf("%d %d", &n, &m);

    char mapa[500][501];
    for (int i = 0; i < n; i++) {
        scanf("%s", mapa[i]);
    }

    int poder[10];
    for (int i = 0; i < 10; i++) {
        scanf("%d", &poder[i]);
    }

    int mudou;

    do {
        mudou = 0;
        char novo_mapa[500][501];

        // Copiar o mapa para o novo_mapa
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                novo_mapa[i][j] = mapa[i][j];
            }
            novo_mapa[i][m] = '\0';  // terminar string
        }

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (mapa[i][j] == '#') continue;

                int especie_atual = mapa[i][j] - '0';

                // Verificar os 4 vizinhos
                for (int d = 0; d < 4; d++) {
                    int nx = i + dx[d];
                    int ny = j + dy[d];

                    if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
                    if (mapa[nx][ny] == '#') continue;

                    int especie_vizinha = mapa[nx][ny] - '0';

                    if (poder[especie_atual] > poder[especie_vizinha]) {
                        novo_mapa[nx][ny] = mapa[i][j];
                        mudou = 1;
                    }
                }
            }
        }

        // Atualiza o mapa com as mudanças feitas
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                mapa[i][j] = novo_mapa[i][j];
            }
        }

    } while (mudou);

    // Imprimir o mapa final
    for (int i = 0; i < n; i++) {
        printf("%s\n", mapa[i]);
    }

    return 0;
}
