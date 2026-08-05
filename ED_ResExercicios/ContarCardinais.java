import java.util.Scanner;

public class ContarCardinais {
    public static void main(String arg[]) {
        Scanner scanner = new Scanner(System.in);

        int linhas = scanner.nextInt();
        int colunas = scanner.nextInt();
        scanner.nextLine();

        char data[][] = new char[linhas][colunas];

        for (int i = 0; i < linhas; i++) {
            String l = scanner.nextLine();
            for (int j = 0; j < colunas; j++) {
                data[i][j] = l.charAt(j);
            }
        }

        int maximo = 0;
        int repetido = 0;

        // Check ROWS for consecutive sequences
        for (int i = 0; i < linhas; i++) {
            int contador = 0;
            for (int j = 0; j < colunas; j++) {
                if (data[i][j] == '#') {
                    contador++;
                } else {
                    // When we find a non-#, check the current sequence
                    if (contador > maximo) {
                        maximo = contador;
                        repetido = 1;
                    } else if (contador == maximo && contador > 0) {
                        repetido++;
                    }
                    contador = 0; // Reset counter for new sequence
                }
            }
            // Check the sequence at the end of the row
            if (contador > maximo) {
                maximo = contador;
                repetido = 1;
            } else if (contador == maximo && contador > 0) {
                repetido++;
            }
        }

        // Check COLUMNS for consecutive sequences
        for (int j = 0; j < colunas; j++) {
            int contador = 0;
            for (int i = 0; i < linhas; i++) {
                if (data[i][j] == '#') {
                    contador++;
                } else {
                    // When we find a non-#, check the current sequence
                    if (contador > maximo) {
                        maximo = contador;
                        repetido = 1;
                    } else if (contador == maximo && contador > 0) {
                        repetido++;
                    }
                    contador = 0; // Reset counter for new sequence
                }
            }
            // Check the sequence at the end of the column
            if (contador > maximo) {
                maximo = contador;
                repetido = 1;
            } else if (contador == maximo && contador > 0) {
                repetido++;
            }
        }
        
        System.out.println(maximo + " " + repetido);
    }
}