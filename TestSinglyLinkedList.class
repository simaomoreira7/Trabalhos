// -----------------------------------------------------------
// Estruturas de Dados (CC1007) - DCC/FCUP
// https://www.dcc.fc.up.pt/~fds/aulas/EDados/2526/
// -----------------------------------------------------------
// Exemplo de utilizacao do TAD Pilha
// -----------------------------------------------------------

import java.util.ArrayList;
import java.util.List;

public class TestMyStack {  

   public static void main(String[] args) {


      MyStack<Integer> s = new LinkedListStack<>();
      
        s.push(5);
        s.push(4);
        s.push(3);
        s.push(2);
        s.push(1);

        int n = 3;

        List<Integer> numeros = new ArrayList<>();
        int tamanho =s.size();

        while (!s.isEmpty()){
            numeros.add(s.top());
            s.pop();
        }

        System.out.println(s.toString());
        System.out.println(numeros);

        for (int i = tamanho-1; i > n-1; i--){
            s.push(numeros.get(i));
        }

        
        
        for (int i = 0; i <= n - 1 ; i++){
            s.push(numeros.get(i));
        }

        System.out.println(s.toString());
        

    }
}