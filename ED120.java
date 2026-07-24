import java.util.Scanner;

public class ED006{
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        scanner.nextLine();
        int clock = 0;

        while(clock < n){


            CircularLinkedList<String> Jogadores = new CircularLinkedList<>();

            String linha = scanner.nextLine();
            String[] frase = linha.split(" ");
            
            int numNomes = scanner.nextInt();
            linha = scanner.nextLine();
            String[] Nomes = linha.split(" ");

            for (int i = 0; i <= numNomes; i++){
                if (Nomes[i] != ""){
                    Jogadores.addLast(Nomes[i]);
                }
            }

            Jogadores.removeFirst();

            

                while(Jogadores.size() != 1){

                    for (int i = 0; i < frase.length-1; i++){
                        Jogadores.rotate();
                    }

                    Jogadores.removeFirst();

                }

                String Carlos = "Carlos";
                if (!Jogadores.getFirst().equals(Carlos)){
                    System.out.println("O Carlos livrou-se (coitado do " + Jogadores.getFirst() + "!)");
                } else {
                    System.out.println("O Carlos nao se livrou");
                }
            clock++;
        }
        
    }

}
