#include <stdio.h>

int main() {
    int n = 0, m = 0, x = 0, y = 0, k = 0;
    scanf("%d %d %d %d %d", &n, &m, &x, &y, &k);

    int deslocx = x - 1 + k;
    int deslocy = y - 1 + k;

    int ciclox = 2 * (n - 1);
    int cicloy = 2 * (m - 1);

    int posfinalx = deslocx % ciclox;
    int posfinaly = deslocy % cicloy;

    if (posfinalx >= n) {
        x = 2 * n - posfinalx - 1;
    } else {
        x = posfinalx + 1;
    }

    if (posfinaly >= m) {
        y = 2 * m - posfinaly - 1;
    } else {
        y = posfinaly + 1;
    }

    printf("%d %d\n", x, y);

    return 0;
}
