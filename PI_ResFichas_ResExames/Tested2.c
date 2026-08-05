/*

1.)
a)(n/100) % 10
b) abs(n)
c) 5 2
d) (n%2)==1
e)
f) c>= '0' && c<= '9'
g) 8
h) s[strlen[s]-1]
i) for int i = 0; i < 4 ; i++
    matrix[i][i] = 22
j) *p ++
k) p -> name
l) i = k + 1
   j = k - 1

2)
2.1)
a) quadratica
b) linear
c) logaritmica

2.2)


3)
int C( int n, int k)
    if (k==n) return 1
    if (k == 0) return 0

    return C(n,k) = C(n-1,k) + C(n-1,k-1)

3.2)
Person comparar(int a, int b)
    if a.age == b.age
        ( a.name > b.name) ? return a.name : return b.name
    else if a.age > b.age
        return a.name
    else
        return b.name

4)
4.1)
Matrix initMatriz(int rows,int cols, int k)
    Matrix m;
    m.rows  = rows
    m.cols = cols
    m.data = malloc(rows * sizeof(int *))
    if (m.data == NULL)
        fodase

    for int i = 0; i<

4.2)
void setValue(Matrix *m, int  row, int cols, int v)
    m->data[row][col] = v
4.3)
void largestsum(Matrix m, int *sumMax, int *rowMax)
    int linhas = m.rows
    int colunas = m.cols

    *sumMax = 0
    *rowMax = 0

    for int i = 0; i< linhas; i++
        int sum = 0
        for int j = 0; j < colunas; j++
            sum += m.data[i][j]
        if (sum > *sumMax)
            *sumMax = sum
            *rowMax = i
4.4)
Matriz transpose (Matrix m)
    initMatriz(int m.cols, int m.rows, 0)
    for int i = 0; i < m.rows; i++
        for int j = 0; j < m.cols;  j++
            m.data[j][i] = m[i][j]
5)
5.a)
contains (LinkedList *l, NodeInfo x)
    Node *p = l-> first
    while (p)
        if ( p -> value == x)
            return True
        p = p->next
    return False
b)
void remove (LinkedList *l,int i)
