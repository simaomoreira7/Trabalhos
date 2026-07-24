import java.util.*;

public class ED165 {

    public static void main(String arg[]){

        Scanner scanner = new Scanner(System.in);

        //Scannes

        int n = scanner.nextInt();
        ArrayList<Integer> numeros = new ArrayList<>();

        for(int i = 0; i < n; i++){
            numeros.add(scanner.nextInt());
        }

        int p = scanner.nextInt();
        ArrayList<Integer> sol = new ArrayList<>();

        for(int i = 0; i < p; i++){
            sol.add(scanner.nextInt());
        }

        // numeros possiveis

        BSTree<Integer> poss = new BSTree<>();
        
        for (int i = 0; i < n; i++){
            for (int j = i; j < n; j++){
                if (!poss.contains(numeros.get(i) + numeros.get(j))){
                    poss.insert(numeros.get(i) + numeros.get(j));
                }
            }
        }


        // verificar 

        for ( int i = 0; i < p;i++){
            if(poss.contains(sol.get(i))){
                System.out.println(sol.get(i) + ": sim");
            } else {
                System.out.println(sol.get(i) + ": nao");
            }

        }


    }
    

}
