import java.util.Scanner;

public class Jogodogalo {
    public static void main(String arg[]) {
        
        Scanner scanner = new Scanner (System.in);

        int n = scanner.nextInt();
        scanner.nextLine();

        char data[][] = new char[n][n];
        boolean incompleto = false;
    
        for (int i = 0; i < n; i++){
            String linha = scanner.nextLine();
            for (int j = 0; j < n; j ++){   
                data[i][j] = linha.charAt(j);
                if (data[i][j] == '.'){
                    incompleto = true;
                }
            }
        }

        boolean ganhoO = false;
        boolean ganhoX = false;

        //Linhas 
        
        for(int i = 0; i < n; i++){
            int contadorO = 0;
            int contadorX = 0;
            for (int j = 0; j < n; j++){
                if (data[i][j] == 'O'){
                    contadorO++;
                }
                if (data[i][j] == 'X'){
                    contadorX++;
                }
            }
            
            if (contadorO == n ){
                ganhoO = true;
            }
            if (contadorX == n){
                ganhoX = true;
            }
        }

        //Colunas 

        for(int i = 0; i < n; i++){
            int contadorO = 0;
            int contadorX = 0;
            for (int j = 0; j < n; j++){
                if (data[j][i] == 'O'){
                    contadorO++;
                }
                if (data[j][i] == 'X'){
                    contadorX++;
                }
            }
            
            if (contadorO == n ){
                ganhoO = true;
            }
            if (contadorX == n){
                ganhoX = true;
            }
        }

        // Diagonal Principal
        int contadorO = 0;
        int contadorX = 0;

        for(int i = 0; i < n; i++){
            if (data[i][i] == 'O'){
                contadorO++;
                if (contadorO == n){
                    ganhoO = true;
                }
            }
            if (data[i][i] == 'X'){
                contadorX++;
                if (contadorX == n){
                    ganhoX= true;
                }
            }
        }
    

        //Diagonal Secundária

        contadorO = 0;
        contadorX = 0;

        for(int i = 0; i < n; i++){
            if (data[i][n-1-i] == 'O'){
                contadorO++;
                if (contadorO == n){
                    ganhoO = true;
                }
            }
            if (data[i][n-1-i] == 'X'){
                contadorX++;
                if (contadorX == n){
                    ganhoX= true;
                }
            }
        }

        if (ganhoX){
            System.out.println("Ganhou o X");
        } else if (ganhoO){
            System.out.println("Ganhou o O");
        } else if (incompleto){
            System.out.println("Jogo incompleto");
        } else {
            System.out.println("Empate");
        }
    }
}