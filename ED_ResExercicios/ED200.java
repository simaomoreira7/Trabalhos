import java.util.Scanner;

public class ED200{

    private static int dx[] = {-1,-1,-1,0,0,1,1,1};
    private static int dy[] = {-1,0,1,-1,1,-1,0,1};

    public static int search(char data[][], int x, int y, boolean autentication[][]){

        if ( x < 0 || x >= data.length || y <0 || y >= data[0].length){
            return 0;
        }


        if (data[x][y] == '.' || autentication[x][y]){
            return 0;
        } 

        autentication[x][y] = true;        
        int sum = 1;

        for ( int i = 0; i < 8; i++){


                int nx = x + dx[i];
                int ny = y + dy[i];
            
                sum += search(data, nx, ny, autentication);

        }

        return sum;

    }



    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in); 

        int ncasos = scanner.nextInt();
        int cont = 0;

        while ( cont < ncasos ){

            //Scannes

            int l = scanner.nextInt();
            int c = scanner.nextInt();

            scanner.nextLine();

            char data[][] = new char[l][c];
            boolean autentication[][] = new boolean[l][c]; 

            for (int i = 0; i < l; i++){
                String linha = scanner.nextLine();
                for (int j = 0; j < c; j++){
                    data[i][j] = linha.charAt(j);
                }
            }
    
            // Procura 

            int maximo = 0;
            int atual = 0;

            for (int i = 0; i < l; i++){
                for (int j = 0; j < c; j++){
                    if (data[i][j] == '#' && autentication[i][j] == false){

                        atual = search(data,i,j,autentication);

                        if(atual > maximo){
                            maximo = atual;
                        }

                    }
                   
                }
            }

            System.out.println(maximo);

            cont++;
        }

    }
}