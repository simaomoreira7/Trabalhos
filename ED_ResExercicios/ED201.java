import java.util.*;

public class ED201{

    static int maximo = 0;

    public static void somas(int indice, ArrayList<Integer> lista, int limit, int soma, int n){

        if (indice == n){
            
            if (soma > maximo && soma <= limit){
                maximo = soma;
            } 
            return;
        }

        if (soma > limit){
            return;
        }

        if (soma > maximo && soma <= limit){
            maximo = soma;
        }


        somas(indice + 1, lista, limit, soma , n);
        somas(indice + 1, lista, limit, soma + lista.get(indice), n);


    }


    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);


        int limit = scanner.nextInt();

        int n = scanner.nextInt();

        ArrayList<Integer> lista = new ArrayList<>();

        for (int i = 0; i < n; i++){
            int numero = scanner.nextInt();
            lista.add(numero);
        
        }

        somas(0, lista, limit, 0, n );

        System.out.println(maximo);

    }
}
