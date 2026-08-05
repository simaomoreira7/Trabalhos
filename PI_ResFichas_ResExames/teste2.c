/*

GRUPO I

1.)
a) (n % 10)
b) if ( a > b) return a
    else return b
c)  7+3
d) (n%2) == 0
e)  int sum = 0;
    while (n > 0){
        int temp = (n % 10)
        sum += temp
        n = n / 10
    return sum
f) c > = 'A' && c <= 'Z'
g) 24
h) s[0]
i ) for (int i = 0 ; i < 5; i++)
    arr[i] = 10 ;
j) (*ptr)--
k) student.grade

l) A = arr[i] > max
   B = max = arr[i]

GRUPO II

GRUPO III

3.)
3.1)
F(int n)
    if (n == 0) return 0
    if (n == 1) return 1

    return F(n-1) + F(n-2)

3.2)
int compareBooks(const void *a, const void *b) {
    const Book *bookA = (const Book *)a;
    const Book *bookB = (const Book *)b;

    if (bookA->rating > bookB->rating)
        return -1;
    else if (bookA->rating < bookB->rating)
        return 1;
    else {
        if (bookA->year > bookB->year)
            return -1;
        else if (bookA->year < bookB->year)
            return 1;
        else
            return 0;
        }
}

4.)
4.1)
Vector* createVector(int initialCapacity) {
// Aloca memória para a struct Vector
    Vector *v = (Vector *) malloc(sizeof(Vector));

// Verifica se a alocação foi bem-sucedida
    if (v == NULL) return NULL;

// Aloca o array de inteiros com a capacidade inicial
    v->elements = (int *) malloc(initialCapacity * sizeof(int));

    if (v->elements == NULL) {
        free(v); // limpa a struct se falhar o array
        return NULL;
}

// Inicializa os campos
v->size = 0;
v->capacity = initialCapacity;

return v;
}
4.2)
void addElement(Vector *v, int element) {
// Passo 1: verifica se vetor está cheio
    if (v->size == v->capacity) {
// Passo 2: dobra a capacidade
    v->capacity = v->capacity * 2;
// realoca o vetor para a nova capacidade
    v->elements = realloc(v->elements, v->capacity * sizeof(int));
// (Idealmente, verificar se realloc devolveu NULL para erro)
}
// Passo 3: adiciona o elemento no final
    v->elements[v->size] = element;
// Passo 4: incrementa o tamanho atual
    v->size++;
}

4.3)
int findElement(Vector v, int element) {
    for (int i = 0; i < v.size; i++) {      // percorre só os elementos existentes
        if (v.elements[i] == element)       // verifica se o elemento atual é o procurado
            return i;                       // retorna índice se encontrado
    }
    return -1;                              // retorna -1 se não encontrar
}

4.4)
Vector mergeVectors(Vector v1, Vector v2)
    Vector v3 = createVector (v1.size + v2.size)
    v3.size = v1.size + v2.size


    int posv1 = 0
    int posv2 = 0

    while posv1 < v1.size || posv2 < v2.size
        if v1.element[posv1] >= v2.element[posv2]
            v3.element[posv1+posv2] = v1.element[posv1]
            posv1 ++;
        else
            v3.element[posv1+posv2] = v2.element[posv2]
            posv2++;

    while posv1 < v1.size
        v3.element[posv1+posv2] = v1.element[posv1]
        posv1++;

    while posv2 < v2.size
        v3.element[posv1+posv2] = v2.element[posv2]
        posv2++;

    return v3

5.1)
int isEmpty(CircularList *list)
    if list -> size == 0
        return 1
    else return 0;

5.2) --VerMElhor



