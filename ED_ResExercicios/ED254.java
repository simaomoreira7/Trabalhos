import java.util.Scanner;

public class ED254 {
    public static void main(String[] args) {
    
        Scanner scanner = new Scanner(System.in);

        int c = scanner.nextInt();

        int contador = 0;

        while (contador < c){
            
            scanner.nextLine();
            int n = scanner.nextInt();

            for ( int i = 0; i < n; i++){
                for (int j = 0; j < n; j++){
                    int esquerda = i;
                    int direita = n-i-1;
                    if (direita > esquerda){
                        if (esquerda == j || direita == j){
                            System.out.print('#');
                        } else{
                            System.out.print('.');
                        }
                    } else {
                        if (j == n/2){
                            System.out.print('#');
                        } else {
                            System.out.print('.');
                        }
                    }
                }
                System.out.println();
            }
            contador ++;
        }

    }
}   
