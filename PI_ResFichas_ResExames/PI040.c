#include <stdio.h>

int main() {

    int a;
    scanf("%d", &a);
    
    int petalas[a];
    for (int i = 0; i < a; i++) {
        petalas[i] = i + 1;
    }

    int naozeros=a;
    int contador = 1;
    while (naozeros > 1) {
        for (int i = 0; i < a; i++) {
            if (petalas[i] != 0){
                if (contador % 2 == 0) {
                    petalas[i] = 0;
                    naozeros--;
                }
            contador++;
            }
        }
    }

    int soma = 0;
    for (int i = 0; i < a; i++) {
        soma += petalas[i];
    }
    printf("%d\n", soma);
    return 0;
}