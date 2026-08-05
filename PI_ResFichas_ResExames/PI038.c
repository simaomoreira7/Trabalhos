#include <stdio.h>

int main() {

    int a = 0;
    scanf("%d", &a);

    int lista1[a];
    for (int i = 0; i < a; i++) {
        scanf("%d", &lista1[i]);
    }

    int b = 0;
    scanf("%d", &b);

    int lista2[b];
    for (int i = 0; i < b; i++) {
        scanf("%d", &lista2[i]);
    }

    int listafinal[a+b];
    int i = 0, j = 0, k = 0;

    while (i < a && j < b) {
        if (lista1[i] < lista2[j]) {
            listafinal[k] = lista1[i];
            i++;
        } else {
            listafinal[k] = lista2[j];
            j++;
        }
        k++;
    }

    while (i < a) {
        listafinal[k] = lista1[i];
        i++;
        k++;
    }

    while (j < b) {
        listafinal[k] = lista2[j];
        j++;
        k++;
    }

    for (int l = 0; l < a+b; l++) {
        if (l == a+b-1) {
            printf("%d\n", listafinal[l]);
        } else {
            printf("%d ", listafinal[l]);
        }
    }
    return 0;
}