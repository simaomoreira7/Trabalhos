import java.util.Scanner;

public class TurtleWorld {

    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);
        int flag = scanner.nextInt();
        int l = scanner.nextInt();
        int c = scanner.nextInt();
        scanner.nextLine();

        char data[][] = new char[l][c];

        for (int i = 0; i < l; i++){
            for (int j = 0; j < c; j++){
                data[i][j] = '.';
            }
        }
        
        int posx = 0;
        int posy = 0;
        boolean escreve = false;
        int dirx = 0;
        int diry = 1;

        String comando = scanner.nextLine();

        while (!comando.equals("end")) { 
            
            if (comando.charAt(0) == 'D'){
                escreve = true;
                data[posx][posy] = '*'; // Marcar posição atual
            }
            
            if (comando.charAt(0) == 'F'){
                String[] partes = comando.split(" ");
                int steps = Integer.parseInt(partes[1]);

                for (int i = 0; i < steps; i++){
                    int novox = posx + dirx;
                    int novoy = posy + diry;
                    
                    if (novox >= 0 && novox < l && novoy >= 0 && novoy < c) {
                        posx = novox;
                        posy = novoy;
                        if (escreve){
                            data[posx][posy] = '*';
                        }
                    } else {
                        break;
                    }
                }
            }

            if (comando.charAt(0) == 'U'){
                escreve = false;
            }

            if (comando.charAt(0) == 'L' || comando.charAt(0) == 'R'){
                dir(comando.charAt(0));
            }

            comando = scanner.nextLine();
        }

        // Processar conforme a flag
        if (flag == 0) {
            for (int i = 0; i < l; i++){
                for (int j = 0; j < c; j++){
                    System.out.print(data[i][j]);
                    if (j < c - 1) System.out.print(" ");
                }
                System.out.println();
            }
        } 
        else if (flag == 1) {
            // Calcular estatísticas
            int total = l * c;
            int marcados = 0;
            int linhasVazias = 0;
            int colunasVazias = 0;
            
            // Contar posições marcadas e linhas vazias
            for (int i = 0; i < l; i++) {
                boolean linhaTemMarcas = false;
                for (int j = 0; j < c; j++) {
                    if (data[i][j] == '*') {
                        marcados++;
                        linhaTemMarcas = true;
                    }
                }
                if (!linhaTemMarcas) linhasVazias++;
            }
            
            // Contar colunas vazias
            for (int j = 0; j < c; j++) {
                boolean colunaTemMarcas = false;
                for (int i = 0; i < l; i++) {
                    if (data[i][j] == '*') {
                        colunaTemMarcas = true;
                        break;
                    }
                }
                if (!colunaTemMarcas) colunasVazias++;
            }
            
            int percentagem = (marcados * 100) / total;
            System.out.println(percentagem + " " + linhasVazias + " " + colunasVazias);
        } 
        else if (flag == 2) {
            // Ler padrão
            int nPadrao = scanner.nextInt();
            int mPadrao = scanner.nextInt();
            scanner.nextLine();
            
            char[][] padrao = new char[nPadrao][mPadrao];
            for (int i = 0; i < nPadrao; i++) {
                String linha = scanner.nextLine();
                String[] partes = linha.split(" ");
                for (int j = 0; j < mPadrao; j++) {
                    padrao[i][j] = partes[j].charAt(0);
                }
            }
            
            // Procurar padrão
            boolean encontrou = false;
            for (int i = 0; i <= l - nPadrao && !encontrou; i++) {
                for (int j = 0; j <= c - mPadrao && !encontrou; j++) {
                    boolean match = true;
                    for (int k = 0; k < nPadrao && match; k++) {
                        for (int m = 0; m < mPadrao && match; m++) {
                            if (padrao[k][m] == '*' && data[i + k][j + m] != '*') {
                                match = false;
                            }
                        }
                    }
                    if (match) {
                        encontrou = true;
                    }
                }
            }
            
            System.out.println(encontrou ? "Sim" : "Nao");
        }
    }

    // Variáveis estáticas para as direções
    static int dirx = 0;
    static int diry = 1;

    public static void dir(char c){
        int tempDirx = dirx;
        int tempDiry = diry;
        
        if (tempDirx == 0 && tempDiry == 1){ // Virado para a direita
            if (c == 'L'){
                dirx = -1;
                diry = 0;
            } else if (c == 'R'){
                dirx = 1;
                diry = 0;
            }
        }
        else if (tempDirx == 1 && tempDiry == 0){ // Virado para baixo
            if (c == 'L'){
                dirx = 0;
                diry = 1;
            } else if (c == 'R'){
                dirx = 0;
                diry = -1;
            }
        }
        else if (tempDirx == 0 && tempDiry == -1){ // Virado para a esquerda
            if (c == 'L'){
                dirx = 1;
                diry = 0;
            } else if (c == 'R'){
                dirx = -1;
                diry = 0;
            }
        }
        else if (tempDirx == -1 && tempDiry == 0){ // Virado para cima
            if (c == 'L'){
                dirx = 0;
                diry = -1;
            } else if (c == 'R'){
                dirx = 0;
                diry = 1;
            }
        }
    }
}


