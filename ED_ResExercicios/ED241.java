import java.util.*;
public class ED241 {


    public static void flag1 (ArrayList<String> nomes){

        ArrayList<String> sol = new ArrayList<>();

        for (int i = 0; i < nomes.size(); i++){

            if(!sol.contains(nomes.get(i))){
                sol.add(nomes.get(i));
            }

        }

        System.out.println(sol.size());

    }


    public static void flag2(ArrayList<String> exercicios){

        BSTMap<String, Integer> mapa = new BSTMap<>();

        for (int i = 0; i < exercicios.size(); i++){

            String exercicio = exercicios.get(i);
            Integer contador = mapa.get(exercicio);

            if (contador == null){

                mapa.put(exercicio, 1);

            } else {

                mapa.put(exercicio, contador + 1);

            }

        }

        int maximo = 0;
        int indice = 0; 

        for (int i = 0; i < exercicios.size(); i++){

            String exercicio = exercicios.get(i);

            if (mapa.get(exercicio) > maximo){
                maximo = mapa.get(exercicio); 
                indice = i;
            }

        }

        System.out.println(exercicios.get(indice) + " " + maximo);

    }

    public static void flag3(ArrayList<String> exercicios, ArrayList<String> avaliado) {

        BSTMap<String, Integer> mapa = new BSTMap<>();

        for (int i = 0; i < exercicios.size(); i++){

            String exercicio = exercicios.get(i);
            Integer contador = mapa.get(exercicio);

            if (contador == null){

                mapa.put(exercicio, 1);

            } else {

                mapa.put(exercicio, contador + 1);

            }

        }

        BSTMap<String, Integer> certos = new BSTMap<>();

        for (int i = 0; i < exercicios.size(); i++){

            String exercicio = exercicios.get(i);
            Integer contador = certos.get(exercicio);

            if (contador == null){
                if (avaliado.get(i).equals("Accepted")){
                    certos.put(exercicio, 1);
                } else {
                    certos.put(exercicio, 0);
                }

            } else {
                if (avaliado.get(i).equals("Accepted")){
                    certos.put(exercicio, contador + 1);
                }

            }

        }

        ArrayList<String> sol = new ArrayList<>();

        for (int i = 0; i < exercicios.size(); i++){

                double racio = (double)certos.get(exercicios.get(i)) / mapa.get(exercicios.get(i));


            if (racio >= 0.5 && !sol.contains(exercicios.get(i))){
                sol.add(exercicios.get(i));
            }

        }

        Collections.sort(sol);

        for (int i = 0; i < sol.size(); i++){
            System.out.println(sol.get(i));
        }

    }


    public static void  flag4(ArrayList<String> nomes,ArrayList<String> exercicios,ArrayList<String> avaliados){


        BSTMap<String, Integer> map = new BSTMap<>();
        ArrayList <String> ED = new ArrayList<>();

        for (int i = 0; i < nomes.size(); i++){

            String nome = nomes.get(i); 
            Integer contador = map.get(nome);
            
            if (contador == null){
                if (avaliados.get(i).equals("Accepted")){
                    map.put(nome, 1);
                } else {
                    map.put(nome, 0);
                }
            }else {

                if (avaliados.get(i).equals("Accepted")){
                    map.put(nome,contador + 1);
                }
            }

            if (!ED.contains(exercicios.get(i))){
                ED.add(exercicios.get(i));
            } 

        }

        ArrayList <String> smarts = new ArrayList<>();

        for (String a : map.keys()){

            if (map.get(a) >= ED.size() && !smarts.contains(a)){
                smarts.add(a);
            }   

        }

        Collections.sort(smarts);

        for (int i = 0; i < smarts.size(); i++){
            String nome = smarts.get(i);
            System.out.println(nome);
        }        

    }




        
    



    
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);


        int flag = scanner.nextInt();

        int n = scanner.nextInt();

        ArrayList<String> nomes = new ArrayList<>();
        ArrayList<String> exercicio = new ArrayList<>();
        ArrayList<String> avaliacao = new ArrayList<>();

        scanner.nextLine();

        for (int i = 0; i < n; i++){

            nomes.add(scanner.next());
            exercicio.add(scanner.next());
            avaliacao.add(scanner.next());

        }
        
        if (flag == 1){
            flag1(nomes);
        }

        if (flag == 2){
            flag2(exercicio);
        }
        
        if (flag == 3){
            flag3(exercicio, avaliacao);
        }

        if (flag == 4){
            flag4(nomes, exercicio, avaliacao);
        }

    }


}
