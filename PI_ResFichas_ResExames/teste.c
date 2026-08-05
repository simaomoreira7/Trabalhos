/* 1.
 a) (n / 100) % 10 --> para ir buscar as centenas
 b) int absoluto = if n < 0 ? -n : n --> ver melhor
 c) saida 5 2
 d) bool impar = n % 2 == 1
 e) int contarDigitos = 0;
    While (n > 0) {
        n /= 10;
        contarDigitos ++
    }
f) bool ehDigito = c >= '0' && c <= '9';
g) 8
h) s[strlen(s) - 1]
i) for (int i = 0; i < 4; i++){
    m[i][i] = 22;
j) (p*)++;
k) printf("%s", p->name);
l) j = k - 1
   i = k + 1

3.)
3.1)
int calcular (int n,int k) {
    if (n==k) return 1;
    if (k == 0) return 1;

    int soma = 0;
    soma+= calcular (n-1,k) + calcular (n-1,k-1);

    return soma;
}

3.2) VER MELHORRRRR
int cmp(Person *a, Person *b){
    if (a -> age == b -> age) return strcmp(a->name,b->name)

    return a -> age - b -> age

4.
4.1)
Matrix initMatrix(int rows,int cols,int k )
    





4.2)
void setValue(Matriz *m, int row, int col, int v){
    m -> data [row][col] = v;
    }

4.3) VER A QUESTÃO DO PONTEIRO PARA M
void largestSum(Matriz m, int *sumMax, int *rowMax){
    *sumMax = *rowMax = 0;
    for (int x = 0; x < m -> rows; x++){
        int sum = 0;
        for (int y = 0; y -> cols; y++){
            sum += m -> data [x][y];
        if (sum > = *sumMax) {
            *sumMax=sum;
            *rowMax = y;
            }
        }
    }
}

4.4)
transpose (Matrix m) {
    Matrix t = init(m->cols,m->rows,0)
    for (int x = 0; x < m -> rows; x++)
        for (int y = 0; y < m -> cols, y ++)
            t-> data[y][x] = m -> data[x][y]
    return t

5.)
5.1)
bool containsInNodes(Node *n, NodeInfo x) {
    if (n == NULL) return false;           // ⚠️ Verifica se chegámos ao fim da lista
    if (n->value == x) return true;        // ✅ Se o valor for igual, encontramos
    return containsInNodes(n->next, x);    // 🔁 Chamada recursiva para o próximo nó
}

bool contains(LinkedList *l, NodeInfo x) {
    return containsInNodes(l->first, x);   // 👈 Começa no primeiro nó
}

5.2)
void removeAt(LinkedList *l, int i) {
    if (i < 0 || i >= l->size) return; // posição inválida

    Node* current = l->first;

    if (i == 0) {

        l->first = current->next;
        free(current);
        l->size--;
        return;
    }


    for (int pos = 0; pos < i - 1; pos++) {
        current = current->next;
    }

    Node* toRemove = current->next;    // nó a remover
    if (toRemove != NULL) {
        current->next = toRemove->next; // faz o nó anterior “pular” o removido
        free(toRemove);                 // libera a memória
        l->size--;                     // diminui o tamanho da lista
    }
}

5.3)
int main() {
    LinkedList s = {0, NULL};  // declara a pilha vazia

    push(&s, 5);   // adiciona 5
    push(&s, 7);   // adiciona 7

    NodeInfo valor = pop(&s);  // remove o topo (que é 7)
    printf("Valor removido do topo: %d\n", valor);

    return 0;
}
*/

#include <stdio.h>

