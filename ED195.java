import java.util.ArrayList;
import java.util.List;

public class ED194{
    public static void reverse(MyStack<Integer> s,int n){

        List<Integer> numeros = new ArrayList<>();
        int tamanho =s.size();

        while (!s.isEmpty()){
            numeros.add(s.top());
            s.pop();
        }

        for (int i = tamanho-1; i > n-1; i--){
            s.push(numeros.get(i));
        }
        
        
        for (int i = 0; i <= n - 1 ; i++){
            s.push(numeros.get(i));
        }

               

    }
}

