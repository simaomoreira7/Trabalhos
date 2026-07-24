import java.util.*;

public class ED234 {

    public static void flag1(ArrayList<String> filmes){

        BSTree<String> mapa = new BSTree<>();
        int contador = 0;

        for (int i = 0; i < filmes.size(); i++){

            if (!mapa.contains(filmes.get(i))){
                mapa.insert(filmes.get(i));
                contador++;
            }
        }
        
        System.out.println(contador);

    }

    public static void flag2(ArrayList<String> filmes, ArrayList<Integer> notas){

        BSTMap<String,Integer> mapa = new BSTMap<>();

        for (int i = 0; i < filmes.size(); i++){

            String filme = filmes.get(i);
            Integer contador = mapa.get(filme);
            
            if (contador == null){
                mapa.put(filme, 1);
            } else {
                mapa.put(filme, contador + 1);
            }

        }   

        int maximo = 0;
        int indice = 0;

        for (int i = 0; i < filmes.size();i++){
            if (mapa.get(filmes.get(i)) > maximo ){
                maximo = mapa.get(filmes.get(i));
                indice = i;
            }
        }

        System.out.println(filmes.get(indice) + " " + maximo);

    }

    public static void flag3(ArrayList<String> filmes, ArrayList<Integer> notas){

        BSTMap<String,Integer> mapa = new BSTMap<>();

        for (int i = 0; i < filmes.size(); i++){

            String filme = filmes.get(i);
            Integer contador = mapa.get(filme);
            
            if (contador == null){
                mapa.put(filme, 1);
            } else {
                mapa.put(filme, contador + 1);
            }

        }   

       BSTMap<String,Integer> somas = new BSTMap<>();

        for (int i = 0; i < filmes.size(); i++){

            String filme = filmes.get(i);
            Integer contador = somas.get(filme);
            
            if (contador == null){
                somas.put(filme, notas.get(i));
            } else {
                somas.put(filme, contador + notas.get(i));
            }

        }   

        ArrayList<String> finalzinho = new ArrayList<>(); 

        for (int i = 0; i < filmes.size(); i++){

            if (!finalzinho.contains(filmes.get(i)) && somas.get(filmes.get(i))/mapa.get(filmes.get(i)) >= 5){
                finalzinho.add(filmes.get(i));
            }

        }

        Collections.sort(finalzinho);

        for (int i = 0; i < finalzinho.size(); i++){
            String palavra  = finalzinho.get(i);
            System.out.println(finalzinho.get(i));
        }


    }

    


    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);

        int flag = scanner.nextInt();

        int n = scanner.nextInt();
        scanner.nextLine();

        ArrayList <String> filmes = new ArrayList<>(); 
        ArrayList <Integer> notas = new ArrayList<>();

        for (int i = 0; i < n; i++){
            
            String filme = scanner.next();
            filmes.add(filme);
            int nota = scanner.nextInt();
            notas.add(nota);
            scanner.nextLine();

        }

        if (flag == 1){
            flag1(filmes);
        }

        if (flag == 2){
            flag2(filmes,notas);
        }

        if (flag == 3){
            flag3(filmes, notas);
        }
    }
}
