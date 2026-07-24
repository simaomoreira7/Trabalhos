import java.util.*;

public class ED242 {

    private static int[] dx = {-1,0,0,1};
    private static int[] dy = {0,1,-1,0};

    static boolean tocaBorda = false;

    public static int tirarilhas(char[][] data, boolean[][] ver, int l, int c, int x, int y){
        // CORREÇÃO: x deve comparar com l (linhas), y com c (colunas)
        if (x < 0 || x >= l || y < 0 || y >= c){
            return 0;
        }

        if(ver[x][y] || data[x][y] == '#'){
            return 0;
        }

        ver[x][y] = true;

        if(x == 0 || x == l-1 || y == 0 || y == c-1){
            tocaBorda = true; 
        }
        
        int tamanho = 1;

        for(int i = 0; i < 4; i++){
            int nx = x + dx[i];
            int ny = y + dy[i];
            tamanho += tirarilhas(data, ver, l, c, nx, ny);
        }

        return tamanho;
    }

    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);

        int K = scanner.nextInt(); // Mudei para K (conforme enunciado)
        scanner.nextLine();

        // Ler o mapa
        ArrayList<String> linhas = new ArrayList<>();
        while(scanner.hasNextLine()){
            String linha = scanner.nextLine().trim();
            if (!linha.isEmpty()) {
                linhas.add(linha);
            }
        }
    
        int l = linhas.size(); // número de linhas
        int c = linhas.get(0).length(); // número de colunas

        char data[][] = new char[l][c];

        for(int i = 0; i < l; i++){
            String frase = linhas.get(i);
            for (int j = 0; j < c; j++){
                data[i][j] = frase.charAt(j);
            }
        }

        // Para K = 0 (eliminar todos os lagos)
        if (K == 0){
            int totalparapreencher = 0;
            boolean ver[][] = new boolean[l][c];

            for (int i = 0; i < l; i++){
                for (int j = 0; j < c; j++){
                    if (data[i][j] == '.' && !ver[i][j]){
                        tocaBorda = false;
                        int tamanhocomponente = tirarilhas(data, ver, l, c, i, j);
                        
                        if (!tocaBorda){ // Se não toca borda, é lago
                            totalparapreencher += tamanhocomponente;
                        }
                    }
                }
            }

            System.out.println(totalparapreencher);
        }

        // Para K = 1 (deixar apenas 1 lago)
        if (K == 1){
            ArrayList<Integer> lagos = new ArrayList<>();
            boolean visitado[][] = new boolean[l][c]; 

            // Primeiro: encontrar todos os lagos e seus tamanhos
            for (int i = 0; i < l; i++){
                for(int j = 0; j < c; j++){
                    if (data[i][j] == '.' && !visitado[i][j]){
                        tocaBorda = false;
                        int lagosize = tirarilhas(data, visitado, l, c, i, j);
                        
                        if(!tocaBorda){ // Se não toca borda, é lago
                            lagos.add(lagosize);
                        }
                    }
                }
            }

            // Ordenar lagos por tamanho (do menor para o maior)
            Collections.sort(lagos);
            
            // Se temos mais de 1 lago, precisamos preencher todos menos 1
            // Para minimizar, preenchemos os menores e deixamos o maior
            int soma = 0;
            
            // Preencher todos os lagos exceto o maior (último após ordenação)
            for(int i = 0; i < lagos.size() - 1; i++){
                soma += lagos.get(i);
            }
            
            System.out.println(soma);
        }

        scanner.close();
    }
}