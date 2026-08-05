
import java.awt.dnd.DragSourceAdapter;

public class SinglyLinkedList<T> {
   
   public class Node<T> {
      private T value;      // Valor guardado no no
      private Node<T> next; // Referencia para o proximo no da lista

      // Construtor
      Node(T v, Node<T> n) {
         value = v;
         next = n;
      }

      // Getters e Setters
      public T getValue() { return value; }
      public Node<T> getNext()  { return next; }
      public void setValue(T v) { value=v; }
      public void setNext(Node<T> n) { next = n; }
   }

   private Node<T> first;    // Primeiro no da lista
   private int size;         // Tamanho da lista

   // Construtor (cria lista vazia)
   SinglyLinkedList() {
      first = null;
      size = 0;
   }

   // Retorna o tamanho da lista
   public int size() {
      return size;
   }

   // Devolve true se a lista estiver vazia ou falso caso contrario
   public boolean isEmpty() {
      return (size == 0);
   }
   
   // Adiciona v ao inicio da lista
   public void addFirst(T v) {
      Node<T> newNode = new Node<T>(v, first); 
      first = newNode;
      size++;
   }

   // Adiciona v ao final da lista
   public void addLast(T v) {
      Node<T> newNode = new Node<T>(v, null); 
      if (isEmpty()) {
         first = newNode;
      } else {
         Node<T> cur = first;
         while (cur.getNext() != null)
            cur = cur.getNext();
         cur.setNext(newNode);         
      }
      size++;
   }

   // Retorna o primeiro valor da lista (ou null se a lista for vazia)
   public T getFirst() {
      if (isEmpty()) return null;
      return first.getValue();
   }

   // Retorna o ultimo valor da lista (ou null se a lista for vazia)
   public T getLast() {
      if (isEmpty()) return null;
      Node<T> cur = first;
      while (cur.getNext() != null)
         cur = cur.getNext();
      return cur.getValue();      
   }

   // Remove o primeiro elemento da lista (se for vazia nao faz nada)
   public void removeFirst() {
      if (isEmpty()) return;
      first = first.getNext();
      size--;
   }

   // Remove o ultimo elemento da lista (se for vazia nao faz nada)
   public void removeLast() {
      if (isEmpty()) return;
      if (size == 1) {
         first = null;
      } else {
         // Ciclo com for e uso de de size para mostrar alternativa ao while
         Node<T> cur = first;
         for (int i=0; i<size-2; i++)
            cur = cur.getNext();
         cur.setNext(cur.getNext().getNext());
      }
      size--;
   }
   
   // Converte a lista para uma String
   public String toString() {
      String str = "{";      
      Node<T> cur = first;
      while (cur != null) {
         str += cur.getValue();
         cur = cur.getNext();
         if (cur != null) str += ",";                     
      }      
      str += "}";
      return str;
   }

   public SinglyLinkedList reverse(){

      SinglyLinkedList<T> inver = new SinglyLinkedList<>();

      Node<T> currNode = first;

      while(currNode!= null){
         inver.addFirst(currNode.getValue());
         currNode = currNode.getNext();
      }

      return inver;

   }

   public int[] occurrences(T elem){

      Node<T> temp = first;
      int c = 0;

      while(temp!= null){
         if (temp.getValue().equals(elem)){
            c++;
         }
         temp = temp.getNext();
      }


      int contador = 0;
      int idx=0;
      Node<T> currNode = first;
      int[] res = new  int[c];

      while(currNode!= null){
         if (currNode.getValue().equals(elem)){
            res[idx] = contador;
            idx++;
         }
         currNode = currNode.getNext();
         contador++;
      }

      if (res.length == 0){
         return null;
      }
      else{
         return res;
      }

   }


   private void removeElem(T elem){
      if(first == null) return; // No need, safeguard

      while(first != null && first.getValue().equals(elem))
         removeFirst();

      Node<T> curr = first;

      while (curr != null && curr.getNext() != null) {
         if(curr.getNext().getValue().equals(elem)){
            curr.setNext(curr.getNext().getNext());
            size--;
         }else
            curr = curr.getNext();
      }
   }

   public void removem(SinglyLinkedList<T> toRemove){
      for(Node<T> node = toRemove.first; this.first != null && node != null; node = node.getNext())
         removeElem(node.getValue());
   }

   public SinglyLinkedList cut(int a, int b){
      SinglyLinkedList<T> nova = new SinglyLinkedList<>();

      if( a < 0 || b > this.size()|| b < a){
         return null;
      } else {
         if (a == 0){
            Node<T> curr = first;
            while ( a <= b){
               nova.addLast(curr.getValue());
               curr = curr.getNext();
               a++;
            } 
            return nova;
         } else {
            Node <T> curr = first;
            int contador = 0;
            while (contador < a){
               curr = curr.getNext();
               contador++;
            }
            while(a <= b ){
               nova.addLast(curr.getValue());
               curr = curr.getNext();
               a++;
            }
            return nova;
         }
      
      }
   }

  public void shift(int k) {
      if (first == null || k == 0) return;
      
      int size = this.size();
      k = k % size;
      if (k == 0) return;
      
      Node<T> last = first;
      while (last.getNext() != null) {
         last = last.getNext();
      }
      
      
      Node<T> newLast = first;
      for (int i = 0; i < size - k - 1; i++) {
         newLast = newLast.getNext();
      }
      
      
      Node<T> newFirst = newLast.getNext();
      newLast.setNext(null);
      last.setNext(first);
      first = newFirst;
   }

   public void duplicate (int pos){

      int contador = 0;
      Node<T> currNode = first;
      while (contador < pos){
         currNode = currNode.getNext();
         contador++;
      }
      Node <T> newNode = new Node<T> (currNode.getValue(), currNode.getNext());
      currNode.setNext(newNode);
      size++;
   }

   public T remove(int pos) {
      
      if (pos < 0 || pos >= size) {
            return null;
         }
         
      T data;
         
      if (pos == 0) {

            data = first.getValue();
            first = first.getNext();

      } else {
            
            Node<T> current = first;
            Node<T> previous = null;
            int count = 0;
            
         while (count < pos) {
                  previous = current;
                  current = current.getNext();
                  count++;
         }
            
         data = current.getValue();
         previous.setNext(current.getNext());
      }
         
      size--;
      return data;
   }

   public SinglyLinkedList<T> copy(){

      SinglyLinkedList<T> nova = new SinglyLinkedList<>();
      Node <T> curNode = this.first;

      while (curNode!= null){
         nova.addLast(curNode.getValue());            
         curNode = curNode.getNext();

      }
      return nova;
   } 

   public void duplicate(){

      Node <T> curNode = first;
      int contador = 0;
      int tamanho = this.size();
      while (contador < tamanho){
         Node <T> newNode = new Node<> (curNode.getValue(), curNode.getNext());
         curNode.setNext(newNode);
         curNode = curNode.getNext().getNext();
         size++;
         contador++;
      }
   }

   public int count(T value){

      Node <T> curNode = first;
      int n = 0;

      while (curNode != null){
         if(curNode.getValue().equals(value)){
            n++;
         }
         curNode=curNode.getNext();
      }

      return n;

   }

   public void removeAll(T value){

      if(first == null) return; 

      while(first != null && first.getValue().equals(value))
         removeFirst();

      Node<T> curr = first;

      while (curr != null && curr.getNext() != null) {
         if(curr.getNext().getValue().equals(value)){
            curr.setNext(curr.getNext().getNext());
            size--;
         }else
            curr = curr.getNext();
      }

   }



}
      

