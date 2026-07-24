import java.util.Scanner;

public class ED235 {

    public static void main(String arg[]){

        Scanner scanner = new Scanner(System.in);

        int c = scanner.nextInt();
        int contador = 0;

        while(contador < c){
            scanner.nextLine();

            int n = scanner.nextInt();

            for (int i = 0; i < n; i++){
                for (int j = 0; j < n; j++){
                    if (j < n-i){
                        System.out.print('#');
                    }else{
                        System.out.print('.');
                    }
                }
                System.out.println();
            }

            contador++;

        }

    }
}