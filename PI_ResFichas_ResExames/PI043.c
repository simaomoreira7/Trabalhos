#include <stdio.h>

int main() {
    int a;
    scanf("%d", &a);

    int numeros[a];
    char simbolos [a-1];

    for (int i = 0; i < a; i++) {
        if (i == a - 1) {
            scanf("%d", &numeros[i]);
        } else {
            scanf("%d %c", &numeros[i], &simbolos[i]);
        }
    }

    for (int i = 0; i < a-1; i++) {
        if (simbolos[i]=='*') {
            numeros[i] = numeros[i] * numeros[i+1];
            numeros[i+1] = 0;
        }
    }

    int soma = 0;

    for (int i = 0; i < a; i++) {
        soma += numeros[i];
    }

    printf("%d\n", soma);

    return 0;
}
