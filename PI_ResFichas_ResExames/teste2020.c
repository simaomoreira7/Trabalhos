/*
 exercicio de stacks exemplo
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define MAX_SIZE 10000

typedef struct {
int stack[MAX_SIZE];
int minStack[MAX_SIZE];
int topIndex;
int minTopIndex;
} MinStack;

// Inicializa a stack
MinStack* minStackCreate() {
MinStack* obj = (MinStack*) malloc(sizeof(MinStack));
obj->topIndex = -1;
obj->minTopIndex = -1;
return obj;
}

// Push de um valor
void minStackPush(MinStack* obj, int val) {
obj->stack[++(obj->topIndex)] = val;
if (obj->minTopIndex == -1 || val <= obj->minStack[obj->minTopIndex]) {
obj->minStack[++(obj->minTopIndex)] = val;
}
}

// Remove o topo
void minStackPop(MinStack* obj) {
if (obj->stack[obj->topIndex] == obj->minStack[obj->minTopIndex]) {
obj->minTopIndex--;
}
obj->topIndex--;
}

// Retorna o topo
int minStackTop(MinStack* obj) {
return obj->stack[obj->topIndex];
}

// Retorna o mínimo
int minStackGetMin(MinStack* obj) {
return obj->minStack[obj->minTopIndex];
}

// Liberta memória (opcional, dependendo do uso)
void minStackFree(MinStack* obj) {
free(obj);
}





