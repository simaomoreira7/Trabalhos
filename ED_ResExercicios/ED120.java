import java.util.Scanner;

public class ED120 {
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();

        int meio = n / 2;

        for (int i = 0; i < n; i++){
            for (int j = 0; j < n; j++){

                if (i <= meio ){

                    if (j < meio -i || j > meio + i){
                        System.out.print('.');
                    } else {
                        System.out.print('#');
                    }
                    
                } else {
                        
                    int contador = i -meio-1;

                    if (j > contador  && j < n- contador-1){
                        System.out.print('#');
                    } else {
                        System.out.print('.');
                    }

                }


            }
            System.out.println();
        }


    }
}
