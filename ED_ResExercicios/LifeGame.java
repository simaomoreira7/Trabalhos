import java.util.Scanner;

public class LifeGame{

    private final static int[] dx = {-1,-1,-1,0,0,1,1,1};
    private final static int[] dy = {1,0,-1,1,-1,1,0,-1};



    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);

        int l = scanner.nextInt();
        int c = scanner.nextInt();
        int total = scanner.nextInt();
        
        scanner.nextLine();

        char data[][] = new char[l][c];

        for (int i = 0; i < l; i++){
            String linha = scanner.nextLine();
            for (int j = 0; j < c; j++){
                data[i][j] = linha.charAt(j);
            }
        }

        int n = 0;

        while (n < total){
                changes(l,c,data);
                n++;
        }
        
        for (int i = 0; i < l; i++){
            for (int j = 0; j < c; j++){
                System.out.print(data[i][j]);
            }
            System.out.println("");
        }
    }

    public static void changes(int l, int c, char data[][]){
        char res[][] = new char[l][c];

        for (int i = 0; i < l; i++){
            for ( int j = 0; j < c; j++){
                int contador = 0;
                for (int dir = 0; dir < 8; dir++){
                    int posx = i + dx[dir];
                    int posy = j + dy[dir];
                    if (0 > posx || posx >= l || 0 > posy || posy >= c){

                    } else {
                        if (data[posx][posy] == 'O'){
                            contador++;
                        }
                    }
                }
                if (data[i][j] == 'O'){
                    if (contador == 2 || contador == 3){
                        res[i][j] = 'O';
                    } else {
                        res[i][j] = '.';
                    }
                } else {
                    if (contador == 3){
                        res[i][j] = 'O';
                    } else {
                        res[i][j] = '.';
                    }
                }
            }
        }

        for (int i = 0; i < l; i++){
            for (int j = 0; j < c; j++){
                data[i][j] = res[i][j];
            }
        }

    }
}


