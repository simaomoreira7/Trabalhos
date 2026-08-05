#include "linkedList.h"

// Forward declaration of function to implement
void duplicate(LinkedList *l);

void printList2(LinkedList *list) {
  Node *curr= list->first;

  printf("{");
  if (curr==NULL) printf("}");
  while (curr != NULL) {
    printf("%d",curr->val);
    curr= curr->next;
    printf("%c",",}"[curr==NULL]);
  }
}
void testInt(LinkedList *list) {
  printf("list = ");
  printList2(list);
  printf("[size=%d]\n", list->size);
  printf("duplicate()");
  duplicate(list);
  printf("\nlist = ");
  printList2(list);
  printf("[size=%d]\n", list->size);
  printf("--------------------------------------\n");
}

int main() {
  int ncases;
  int n;
  int value;
  LinkedList l1;

  scanf("%d",&ncases);            // number of cases
  for (int i=0; i<ncases; i++) {
    initList(&l1);
    scanf("%d",&n);               // number of values in the list
    for (int i=0; i<n; i++) {
      scanf("%d",&value);         // the values
      addLast(&l1, value);
    }
    // test
    testInt(&l1);                 // test this case
  }
}