/*
GRUPO 1
a) (n/10) %10
b) if( a < b && a < c) return a
    else if (b < a && b < c) return b
    else return cchar
c) 4*5
d) n%3==0
e)
int pos = 0;
int contador = 0;
while(frase[pos] != '\0')
    if frase[pos] == 'd'
        contador ++;
    pos++;
return contador
f) c >= 'a' && c <= 'z'
g) 8
h) sizeof(s)
i)
j) *(arr+2)
k) car -> speed = 120
l) A -> size - 1
    B -> arr[i] > arr[i+1]

GRUPO 2
1)
a) O(n^2)
b) O(log n)
c) O(n)
2)

GRUPO 3
3.1)
int GDC( int a, int b)
    if (b == 0) return a

    return GCD(b,a%b)

3.2)
#include <string.h> // para strcmp

int compareStudents(const void *a, const void *b) {
const Student *studentA = (const Student *)a;
const Student *studentB = (const Student *)b;

if (studentA->average > studentB->average)
return -1; // ordem decrescente
else if (studentA->average < studentB->average)
return 1;
else {
if (studentA->age < studentB->age)
return -1; // mais novo vem primeiro
else if (studentA->age > studentB->age)
return 1;
else
return 0;
}
}

GRUPO 4
4)
Stack createStack (int initialCapacity)
    Stack s
    s.data = (int *)malloc(initialCapacity*sizeof(int))

    if ( s.data == NULL)
        s.top = -1
        s.capacaity = 0
        return s

    s.top = -1
    s.capacity = initialCapacity;

    return s;

4.3)
int pop(Stack *s)
     if (s->top == -1 )
        return -1;
     else
        s->top--;
        return s->data[s->top];

4.4)
int isEmpty(Stack s)
    if (s.top==-1)
        return 1
    else return 0
