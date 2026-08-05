
// http://www.dcc.fc.up.pt/~fds/aulas/EDados/2425/
// -----------------------------------------------------------
// Exemplo de utilizacao da lista ligada simples
// Ultima alteracao: 01/04/2018
// -----------------------------------------------------------

public class TestSinglyLinkedList {

   public static void main(String[] args) {

      SinglyLinkedList<Integer> singlyLinkedList1 = new SinglyLinkedList<>();
      SinglyLinkedList<Integer> singlyLinkedList1toRemove = new SinglyLinkedList<>();



      singlyLinkedList1.addLast(2);
      singlyLinkedList1.addLast(4);
      singlyLinkedList1.addLast(6);
      singlyLinkedList1.addLast(8);
      singlyLinkedList1.addLast(10);

      System.out.println("Pre: " + singlyLinkedList1.toString());
      System.out.println("Pre: " + singlyLinkedList1.size());

      singlyLinkedList1.duplicate();
      
      System.out.println("Pos: " + singlyLinkedList1.size());
      System.out.println("Pos: " + singlyLinkedList1.toString());



      SinglyLinkedList<Character> singlyLinkedList2 = new SinglyLinkedList<>();
      SinglyLinkedList<Character> singlyLinkedList3 = new SinglyLinkedList<>();
      SinglyLinkedList<Character> singlyLinkedList4 = new SinglyLinkedList<>();
      SinglyLinkedList<Character> singlyLinkedList5 = new SinglyLinkedList<>();
      SinglyLinkedList<Character> singlyLinkedList6 = new SinglyLinkedList<>();
   }
}