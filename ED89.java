import java.util.Scanner;

public class ED282 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int T = scanner.nextInt();  // Tempo máximo por cliente por turno
        int N = scanner.nextInt();  // Número de clientes
        scanner.nextLine();

        CircularLinkedList<String> nomes = new CircularLinkedList<>();
        CircularLinkedList<Integer> nTvs = new CircularLinkedList<>();
        CircularLinkedList<Boolean> TFA = new CircularLinkedList<>();

        for (int i = 0; i < N; i++) {
            String line = scanner.nextLine();
            String[] parts = line.split(" ");
            nomes.addLast(parts[0]);
            int time = Integer.parseInt(parts[1]);
            nTvs.addLast(time);
        }

        int Tvsdia = 0;
        int TvsTotal = 0;
        int dia = 1;
        String primeiro = nomes.getFirst();

        while (!nomes.isEmpty()){

            String currentN = nomes.getFirst();
            int CurrentTvs = nTvs.getFirst();
        

            if (CurrentTvs <= T){
        
                if(Tvsdia > 0 && currentN.equals(primeiro)){
                    
                    Tvsdia += CurrentTvs;
                    TvsTotal += CurrentTvs;
                    System.out.println(currentN + " " + dia + " " + Tvsdia + " "+ TvsTotal);
                    dia++;
                    Tvsdia=0;

                }

                Tvsdia += CurrentTvs;
                TvsTotal += CurrentTvs;
                System.out.println(currentN + " " + dia + " " + Tvsdia + " "+ TvsTotal);
                nTvs.removeFirst();
    
            } else {

                if(Tvsdia > 0 && currentN.equals(primeiro)){
                    dia++;
                    
                } else { 
                    Tvsdia += T;
                    TvsTotal += T;
                    nomes.rotate();
                    nTvs.removeFirst();
                    nTvs.addLast(CurrentTvs-T);
                }

            
            }

    
        }

    }
}
