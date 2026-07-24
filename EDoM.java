import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;


public class ED89 {
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);
        List <Integer> NIF = new ArrayList<>();
        List <String> NomeEmpresa = new ArrayList<>();
        List <String> AtivEconomica = new ArrayList<>();
        List <Integer> Cod = new ArrayList<>();
        List <Integer> Rendimentos = new ArrayList<>();
        
        int n = scanner.nextInt();
        int contador = 0;
        int flag = scanner.nextInt();
        scanner.nextLine();

        while(contador < n){
            
            int nif = scanner.nextInt();
            scanner.nextLine();
            String nomeempresa = scanner.nextLine();
            String ativeconomica = scanner.nextLine();
            int cod = scanner.nextInt();
            scanner.nextLine();
            int rendimentos = scanner.nextInt();
            scanner.nextLine();


            NIF.add(nif);
            NomeEmpresa.add(nomeempresa);
            AtivEconomica.add(ativeconomica);
            Cod.add(cod);
            Rendimentos.add(rendimentos);
        
            contador ++;
        
        }

        if (flag == 0){
            flag0(n,AtivEconomica);
        }
        if (flag == 1){
            flag1(n, Cod, Rendimentos);
        }


    }

    public static void flag0(int n, List <String> AtivEconomica){
        
        List <String> autentication = new ArrayList<>();

        for (int i = 0; i < n; i++){
            String atividade = AtivEconomica.get(i);
            if (!autentication.contains(atividade)){
                autentication.add(atividade);
            }
        }
        
        System.out.println(autentication.size());

    }

    public static void flag1(int n, List <Integer> Cod, List <Integer> Rendimentos){
        
        List <Integer> Codigos = new ArrayList<>();
        List <Integer> Somas = new ArrayList<>();

        for (int i = 0; i < n; i++){
            int c = Cod.get(i);
            if (!Codigos.contains(c)){
                Codigos.add(c);
            }
        }
        
        for (int i = 0; i < Codigos.size(); i++ ){
            int soma = 0;
            for (int j = 0; j < n; j++){
                if (Codigos.get(i) == Cod.get(j)){
                    soma +=  Rendimentos.get(j);
                }
            }
            Somas.add(soma);
        }

        for ( int i = 0; i < Codigos.size(); i++){
            System.out.println(Codigos.get(i)+" "+Somas.get(i));
        }

    }


}