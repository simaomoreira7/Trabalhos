import java.util.Scanner;

public class SopaDeLetras{

    private final static int[] dx = {-1,0,0,1};
    private final static int[] dy = {0,-1,1,0}; 
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner (System.in);
        boolean motor = true;
        int contador = 0;
        while (motor){

            contador++;
            
            int l = scanner.nextInt();
            int c = scanner.nextInt();
            scanner.nextLine();
            
            if (l == 0 || c == 0 ){
                motor = false;
                break;
            }

            char data[][] = new char[l][c];
            for (int i = 0; i < l; i++){
                String linha = scanner.nextLine();
                for (int j = 0; j < c; j ++){
                    data[i][j] = linha.charAt(j);
                }
            }

            boolean tabela[][] = new boolean[l][c];

            int numero = scanner.nextInt();
            scanner.nextLine();

            for (int i = 0; i < numero; i++){
                String palavra = scanner.nextLine();
                searchinitial(l,c,data,palavra,tabela);
            }
            
            System.out.println("Input #"+contador);

            escrever(l, c, data, tabela);

        }
    }

    public static void searchinitial(int l, int c, char data[][], String palavra,boolean tabela[][]) {
        
        for (int i = 0; i < l; i ++){
            for (int j = 0; j < c; j++){
                if (data[i][j] == palavra.charAt(0)){
                    searchallword(l,c,data,palavra,tabela,i,j);
                }
            }
        }

    }

    public static void  searchallword(int l,int c,char data[][], String palavra,boolean tabela[][],int x ,int y){
        for (int dir = 0; dir < 4; dir ++){
            if (searchIndirection(l,c,data,palavra,tabela, x,y,dx[dir],dy[dir])){
            }
        }
    }

    public static boolean searchIndirection(int l, int c, char data[][], String palavra,boolean tabela[][], int startX, int startY, int dirX, int dirY) {
        int len = palavra.length();
        
        int endX = startX + (len - 1) * dirX;
        int endY = startY + (len - 1) * dirY;
        
        if (endX < 0 || endX >= l || endY < 0 || endY >= c) {
            return false;
        }

        for (int k = 0; k < len; k++) {
            int currentX = startX + k * dirX;
            int currentY = startY + k * dirY;
            
            if (data[currentX][currentY] != palavra.charAt(k)) {
                return false;
            }
        }
         for (int k = 0; k < len; k++) {
            int currentX = startX + k * dirX;
            int currentY = startY + k * dirY;
            tabela[currentX][currentY] = true;
        }
        
        return true;
    }

    public static void escrever (int l, int c, char data[][], boolean tabela[][] ){
        for (int i = 0; i < l; i++){
            for (int j = 0; j < c; j++){
                if (tabela[i][j] == false){
                    System.out.print('.');
                } else {
                    System.out.print(data[i][j]);
                }
            }
            System.out.println();
        }
    }

}


