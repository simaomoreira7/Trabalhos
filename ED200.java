import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


public class ED198 {
    
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);

        int x = scanner.nextInt();

        List<Integer> lista = new ArrayList<>();

        for (int i = 0; i < x; i++){
            lista.add(scanner.nextInt());
        }

        int valor = somas(lista);


        System.out.println(valor);

    }

    public static int  somas(List <Integer> lista) {
        
        int maxGlobal = lista.get(0);
        int maxAtual = lista.get(0);

        for (int i = 1; i < lista.size(); i++){
            maxAtual = Math.max(lista.get(i), lista.get(i) + maxAtual);

            if (maxAtual > maxGlobal){
                maxGlobal = maxAtual;
            }

        }

        return maxGlobal;
    }
}
