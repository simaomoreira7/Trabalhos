import java.util.*;

public class ED231 {
    public static void main(String arg[]){

        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        scanner.nextLine();

        List<Integer> valores = new ArrayList<>();
        
        for (int i = 0; i < n; i++){
            int numero = scanner.nextInt();
            valores.add(numero);
        }

        scanner.nextLine();
        int flag = scanner.nextInt();

        if (flag == 1){
            flag1(n, valores);
        } else if (flag == 2){
            flag2(n, valores);
        } else if (flag == 3){
            flag3(n, valores);
        }
    }

    public static void flag1(int n, List <Integer> valores){
        
        List <Integer> diferencas = new ArrayList<>();
        
        if (n <= 1){
            int maximo = 0;
            int minimo = 0;

            System.out.println(minimo + " " + maximo);

        } else {

            for (int i = 1; i < n; i++){
                int pre = valores.get(i-1);
                int pos = valores.get(i);
                int diferenca = pos - pre;
                diferencas.add(diferenca);
            }

            int maximo = diferencas.get(0);
            int minimo = diferencas.get(0);

            for(int i = 0; i < n-1; i++){
                if (minimo > diferencas.get(i)){
                    minimo = diferencas.get(i);
                }
                if (maximo < diferencas.get(i)){
                    maximo = diferencas.get(i);
                }
            }
            System.out.println(minimo + " " + maximo);
        
        }

    }

    public static void flag2(int n, List <Integer> valores){
        
        boolean intervalosVerde = true;
        int verdes=0;
        int contador = 0;
        int maximo = 0;
        for (int i = 1; i < n; i++) {
           
            int diferenca = valores.get(i) - valores.get(i - 1);
            double percentagem = (double) diferenca / valores.get(i - 1) * 100;
    
            if ((percentagem) <= 5){
                verdes++;
                if (verdes > maximo){
                    maximo = verdes;
                }
                if(intervalosVerde){
                    contador++;
                    intervalosVerde = false;
                }
            } else {
                intervalosVerde = true;
                verdes = 0;
            }
        }

        System.out.println(contador+" "+maximo);

    }

    public static void flag3(int n, List <Integer> valores){
        
        int maximo = 0;
        for (int i = 0; i < n; i++) {
            if (valores.get(i) > maximo){
                maximo = valores.get(i);
            }
        }

        for (int i = maximo/100; i > 0; i--) {
            for (int j = 0; j < n; j++) {
                if (valores.get(j) / 100 >= i)
                    System.out.print('#');
                else 
                    System.out.print('.');
            }
            System.out.println();
        }
    }

}   
