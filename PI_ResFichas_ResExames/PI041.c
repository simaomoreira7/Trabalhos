#include <stdio.h>

void terrarea(int lugares[], int despejo, int terra, int a) {
    int pos = despejo - 1;

    lugares[pos] += terra; // Corrigido para acumular
    terra--;

    int offset = 1;

    while (terra > 0) {
        int left = pos - offset;
        int right = pos + offset;

        if (left >= 0 && terra > 0) {
            lugares[left] += terra;
        }

        if (right < a && terra > 0) {
            lugares[right] += terra;
        }
        offset++;
        terra--;
    }
}


int main() {

    int a = 0;
    scanf("%d", &a);
    int lugares[a];
    for (int i = 0; i < a; i++) {
        lugares[i] = 0;
    }

    int ncamioes;
    scanf("%d", &ncamioes);

    int despejar[ncamioes];
    int terra[ncamioes];

    for (int i = 0; i < ncamioes; i++) {
        scanf("%d", &despejar[i]);
        scanf("%d", &terra[i]);
    }

    int despejo = 0;
    int terras = 0;

    for (int i = 0; i < ncamioes; i++) {
        despejo = despejar[i];
        terras = terra[i];
        terrarea(lugares, despejo, terras, a);
    }

    for (int i = 0; i < a; i++) {
        if (i == a - 1) {
            printf("%d", lugares[i]);
        }else {
            printf("%d ", lugares[i]);
        }
    }
    printf("\n");
    return 0;
}