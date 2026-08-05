import  java.util.Scanner;

public class EDoM {
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();

        int contador = 1;

        for (int i = 0; i < n; i++){
            for (int j = 0 ; j < n; j++){
                
                if (contador == n/2){
                    contador = 0;
                }

                if (contador == 1){
                    contador = 0;
                }
                
                
                if (j == 0 || j == n - 1 || j == contador || j == n - contador -1){
                    System.out.print('#');
                } else {
                    System.out.print('.');
                }

                contador++;
            }
            System.out.println();
        }




    }
}
