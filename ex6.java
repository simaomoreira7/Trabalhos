import java.util.Scanner;

public class ex5 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        int inicio = scanner.nextInt();
        int fim = scanner.nextInt();
        int conta = 0;

        for (int i = inicio; i < fim+1; i++){
            if (primos(i)){
                conta++;
            }
        }

        System.out.println(conta);

        scanner.close();
    }

    public static boolean primos (int numero){

        if (numero ==2) return true;

        if (numero % 2 == 0) return false;

        for (int i = 3; i * i <= numero; i+=2){
            if (numero % i == 0){
                return false;
            }
        }
        return true;
    }
}