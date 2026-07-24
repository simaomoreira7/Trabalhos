import java.util.Scanner;

public class ex2 {
    public static void main(String arg[]){
        Scanner scanner = new Scanner (System.in);
        
        int numero = scanner.nextInt();
        scanner.nextLine();
        System.out.println(numero);

        for(int i = 0; i < numero; i++ ){

            String frase =  scanner.nextLine();

            frase = frase.toLowerCase();

            frase = frase.replaceAll("[^a-z]","");

            int end = frase.length() - 1;
            int inicio = 0;

            boolean palindrome = true;
            
            while (end > inicio){

                if (frase.charAt(inicio) != frase.charAt(end)){
                    palindrome = false;
                    break;
                }

                inicio ++;
                end--;
            }
            
            if (palindrome){
                System.out.println("sim");
            } else {
                System.out.println("nao");
            }
        }
        scanner.close();
    }
}