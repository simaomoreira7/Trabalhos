public class TestMyQueue {
   
   public static MyQueue<Integer> merge(MyQueue<Integer> a, MyQueue<Integer> b){

      MyQueue <Integer> nova = new LinkedListQueue<Integer>();

      int valorA = a.dequeue();
      int valorB = b.dequeue();

      while (true){

         if (valorA < valorB){
            nova.enqueue(valorA);
            if(a.isEmpty()){
               nova.enqueue(valorB);
              break; 
            } else{
               valorA = a.dequeue();
            }

         } else {
            nova.enqueue(valorB);
             if(b.isEmpty()){
               nova.enqueue(valorA);
              break; 
            } else{
               valorB = b.dequeue();
            }

         }

      }

      while(!a.isEmpty()){
         nova.enqueue(a.dequeue());
      }

       while(!b.isEmpty()){
         nova.enqueue(b.dequeue());
      }

      return nova;
   }
   
   
   
   public static void main(String[] args) {

      // Criacao da fila
      MyQueue<Integer> a = new LinkedListQueue<Integer>();
      MyQueue<Integer> b = new LinkedListQueue<Integer>();

      a.enqueue(2);
      a.enqueue(4);
      a.enqueue(8);
      a.enqueue(10);
      b.enqueue(1);
      b.enqueue(4);
      b.enqueue(9);
      
      


      System.out.println(merge(a, b));
 
   }
}
