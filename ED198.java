public class ED197 {
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
   
}
