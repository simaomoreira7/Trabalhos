
import java.nio.file.Path;

// -----------------------------------------------------------
// Estruturas de Dados 2025/2026 (CC1007) - DCC/FCUP
// https://www.dcc.fc.up.pt/~fds/aulas/EDados/2526/
// -----------------------------------------------------------
// Arvore binaria "normal"
// -----------------------------------------------------------

public class BTree<T> {   
   private BTNode<T> root; // raiz da arvore

   // Construtor
   BTree() {
      root = null;
   }

   // Getter e Setter para a raiz
   public BTNode<T> getRoot() {return root;}
   public void setRoot(BTNode<T> r) {root = r;}

   // Verificar se arvore esta vazia
   public boolean isEmpty() {
      return root == null;
   }

   // --------------------------------------------------------

   // Numero de nos da arvore   
   public int numberNodes() {
      return numberNodes(root);
   }

   private int numberNodes(BTNode<T> n) {
      if (n == null) return 0;
      return 1 + numberNodes(n.getLeft()) + numberNodes(n.getRight());
   }

   // --------------------------------------------------------

   // Altura da arvore
   public int depth() {
      return depth(root);
   }

   private int depth(BTNode<T> n) {
      if (n == null) return -1;
      return 1 + Math.max(depth(n.getLeft()), depth(n.getRight()));
   }

   // --------------------------------------------------------
   
   // O elemento value esta contido na arvore?
   public boolean contains(T value) {
      return contains(root, value);
   }

   private boolean contains(BTNode<T> n, T value) {
      if (n==null) return false;
      if (n.getValue().equals(value)) return true;
      return contains(n.getLeft(), value) || contains(n.getRight(), value);
   }

   // --------------------------------------------------------

   // Imprimir arvore em PreOrder
   public void printPreOrder() {
      System.out.print("PreOrder:");
      printPreOrder(root);
      System.out.println();
   }

   private void printPreOrder(BTNode<T> n) {
      if (n==null) return;
      System.out.print(" " + n.getValue() );
      printPreOrder(n.getLeft());
      printPreOrder(n.getRight());
   }

   // --------------------------------------------------------
   
   // Imprimir arvore em InOrder
   public void printInOrder() {
      System.out.print("InOrder:");
      printInOrder(root);
      System.out.println();
   }

   private void printInOrder(BTNode<T> n) {
      if (n==null) return;
      printInOrder(n.getLeft());
      System.out.print(" " + n.getValue());
      printInOrder(n.getRight());
   }

   // --------------------------------------------------------

   // Imprimir arvore em PostOrder
   public void printPostOrder() {
      System.out.print("PostOrder:");
      printPostOrder(root);
      System.out.println();
   }

   private void printPostOrder(BTNode<T> n) {
      if (n==null) return;
      printPostOrder(n.getLeft());
      printPostOrder(n.getRight());
      System.out.print(" " + n.getValue());
   }

   // --------------------------------------------------------

   // Imprimir arvore numa visita em largura (usando TAD Fila)
   public void printBFS() {
      System.out.print("BFS:");
      
      MyQueue<BTNode<T>> q = new LinkedListQueue<BTNode<T>>();
      q.enqueue(root);
      while (!q.isEmpty()) {
         BTNode<T> cur = q.dequeue();
         if (cur != null) {
            System.out.print(" " + cur.getValue());
            q.enqueue(cur.getLeft());
            q.enqueue(cur.getRight());
         }
      }
      System.out.println();
   }

   // --------------------------------------------------------
   
   // Imprimir arvore numa visita em profundidade (usando TAD Pilha)
   public void printDFS() {
      System.out.print("DFS:");
      
      MyStack<BTNode<T>> q = new LinkedListStack<BTNode<T>>();
      q.push(root);
      while (!q.isEmpty()) {
         BTNode<T> cur = q.pop();
         if (cur != null) {
            System.out.print(" " + cur.getValue());
            q.push(cur.getLeft());
            q.push(cur.getRight());
         }
      }
      System.out.println();
   }

   

   public int numberLeafs(BTNode<T> N){

      if(N == null){
         return 0;
      }
      
      if (N.getLeft() == null && N.getRight() == null){
         return 1;
      }

      return numberLeafs(N.getLeft()) + numberLeafs(N.getRight());

   }

   public int numberLeafs(){
      return numberLeafs(root);
   }


   public boolean strict(BTNode<T> N){

      if (N == null){
         return true;
      }

      if (N.getLeft() != null && N.getRight() == null || N.getLeft() == null && N.getRight() != null){
         return false;
      }

      return strict(N.getLeft()) && strict(N.getRight());

   }

   public boolean strict(){
      return strict(root);
   }

   public int nodesLevel(int k, BTNode<T> N, int altura){

      if (altura == k){
         if(N != null){
            return 1;
         } else {
            return 0;
         }
      }

      if (N == null){
         return 0;
      }
   
      return nodesLevel(k,N.getLeft(), altura + 1) + nodesLevel(k,N.getRight(),altura+1);
   }



   public int nodesLevel(int k){

      return nodesLevel(k,root,0);

   }

   public int internal(BTNode<T> N){

      if (N == null){
         return 0;
      }

      if(N.getLeft() != null || N.getRight() != null){
         return 1 + internal(N.getLeft()) + internal(N.getRight());
      }  

      return internal(N.getLeft()) + internal(N.getRight());
   }

   public int internal(){

      return internal(root);

   }

   public void cut(int d, BTNode<T> N, int altura){

      if (N == null){
         return;
      }

      if (d == altura){
         N.setLeft(null);
         N.setRight(null);
         return;
      }

      cut(d, N.getLeft(), altura + 1);
      cut(d, N.getRight(), altura + 1);

   }



   public void cut(int d){

      if (d <= 0){
         root = null;
         return;
      }

      cut(d-1, root,0);

   }





}
