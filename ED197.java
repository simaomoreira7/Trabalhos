public class ED196 {
     
    public static void process(MyQueue<String> q, MyQueue<String> a, MyQueue<String> b){

        while(!q.isEmpty()){
            String nome = q.dequeue();
            String letra = q.dequeue();

            if (letra.equals("A")){
                a.enqueue(nome);
            } else if (letra.equals("B")){
                b.enqueue(nome);
            } else if (letra.equals("X")){
                if (a.size() > b.size()){
                    b.enqueue(nome);
                } else if (a.size() < b.size()) {
                    a.enqueue(nome);
                }
            }
          
        }
    }
   
}
