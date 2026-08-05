#include <stdio.h>
#include <string.h>

#define MAX 200
#define SKIPEOL {while (getchar()!='\n') ;}

void verify(char *line) {
    char stack[MAX];
    int top = -1;
    int pos = 0;

    while (line[pos] != '\0' && line[pos] != '\n') {
        char c = line[pos];

        if (c == '(' || c == '[') {
            // Empilha o parêntese de abertura
            if (top == MAX - 1) {
                printf("Erro: Pilha cheia!\n");
                return;
            }
            stack[++top] = c;
        } else if (c == ')') {
            // Verifica se o topo da pilha é '('
            if (top == -1 || stack[top] != '(') {
                printf("Erro na posicao %d\n", pos);
                return;
            }
            top--;
        } else if (c == ']') {
            // Verifica se o topo da pilha é '['
            if (top == -1 || stack[top] != '[') {
                printf("Erro na posicao %d\n", pos);
                return;
            }
            top--;
        }
        pos++;
    }

    // Verifica se ainda há parênteses não fechados
    if (top != -1) {
        printf("Ficam parenteses por fechar\n");
    } else {
        printf("Expressao bem formada\n");
    }
}

int main() {
    int ncases;
    char line[MAX];

    scanf("%d",&ncases);
    SKIPEOL;
    for (int c=0; c<ncases; c++) {
        fgets(line,sizeof(line),stdin);
        verify(line);
    }
    return 0;
}