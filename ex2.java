import java.util.Scanner;

public class ex1 {
    public static void main(String arg[]){
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        
        for (int i = 0; i < (n/2) + 1; i++){
            int p = n/2 - i;
            int q = n/2 + i;
            for (int j = 0; j < n; j++){
                if (p <= j && q >= j){
                    System.out.print('#');
                } else {
                    System.out.print('.');
                }
            }
            System.out.println();
        }

         for (int i = 1; i < (n/2)+1; i++){
            int p = 0 + i;
            int q = n-1 - i;
            for (int j = 0; j < n; j++){
                if (p <= j && q >= j){
                    System.out.print('#');
                } else {
                    System.out.print('.');
                }
            }
            System.out.println();
        }
    }
}