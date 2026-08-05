import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class ex3 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        List<Integer> numeros = new ArrayList<>();
        
        int quantidade = scanner.nextInt();
        int primeiroNumero = scanner.nextInt();
        numeros.add(primeiroNumero);
        
        int maior = primeiroNumero;
        int menor = primeiroNumero;
        int soma = primeiroNumero;
        
        for(int i = 1; i < quantidade; i++) {
            int numero = scanner.nextInt();
            numeros.add(numero);
            
            if (numero > maior) {
                maior = numero;
            }
        
            if (numero < menor) {
                menor = numero;
            }
            soma += numero;
        }

        double media = (double) soma / quantidade;
        int amplitude = Math.abs(maior - menor);

        System.out.printf("%.2f\n", media);
        System.out.println(amplitude);
        
        scanner.close();
    }
}