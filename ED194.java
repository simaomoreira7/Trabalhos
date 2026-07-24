import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ED183 {

    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        double soma = 0;
        List <Integer> numeros = new ArrayList<>();

        for ( int i = 0; i < n; i ++){
            int valor = scanner.nextInt();
            numeros.add(valor);
            soma += valor;

        }

        int minimo = numeros.get(0);
        int maximo = numeros.get(0);

         for ( int i = 0; i < n; i ++){
            if (numeros.get(i) > maximo){
                maximo = numeros.get(i);
            } else if ( numeros. get(i) < minimo ){
                minimo = numeros.get(i);
            }

        }

        int amplitude = Math.abs(maximo - minimo); 

        System.out.printf(String.format("%.2f",soma/n));
        System.out.println();
        System.out.println(amplitude);
    }


}
