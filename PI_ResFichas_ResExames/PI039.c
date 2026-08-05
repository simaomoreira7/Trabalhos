#include <stdio.h>

void shift(int a[], int n, int k) {
    if (k > 0){
        int temp = 0;
        int b[n];
        while (temp < k) {
            b[0] = a[n - 1];
            for (int i = 1; i < n; i++) {
                b[i] = a[i - 1];
            }
            for (int i = 0; i < n; i++) {
                a[i] = b[i];
            }
            temp++;
        }
    }
    if (k < 0) {
        k= k * -1;
        int temp = 0;
        int b[n];
        while (temp < k) {
            b[n-1] = a[0];
            for (int i = 0; i < n-1; i++) {
                b[i] = a[i + 1];
            }
            for (int i = 0; i < n; i++) {
                a[i] = b[i];
            }
            temp++;
        }
    }
}





// print an array of size n (assume size >= 1)
void print_array(int a[], int n) {
    printf("[%d", a[0]);
    for (int i=1; i<n; i++)
        printf(",%d", a[i]);
    printf("]\n");
}

int main(void) {

    // Ler as informações
    int n;
    scanf("%d", &n);
    int a[n];
    for (int i=0; i<n; i++)
        scanf("%d", &a[i]);
    int k;
    scanf("%d", &k);

    // Primeiro Print
    print_array(a, n);

    // Mudar a Lista
    shift(a, n, k);

    //Prints da lista mudada
    printf("After shift(a,%d,%d):\n", n, k);
    print_array(a, n);

    return 0;
}