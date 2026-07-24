import java.util.Scanner;

public class ED237{
    
    public static void main(String[] args) {

        Scanner scanner = new Scanner(System.in);

        int tempoInteracao = scanner.nextInt();
        int nprocesso = scanner.nextInt();
        scanner.nextLine();

        CircularLinkedList<String> processo = new CircularLinkedList<>();
        CircularLinkedList<Integer> tempo = new CircularLinkedList<>();

        for(int i = 0; i < nprocesso;i++){
            String Line = scanner.nextLine();
            String[] parts = Line.split(" ");
            processo.addLast(parts[0]);
            tempo.addLast(Integer.parseInt(parts[1]));
        }

        int currentTime = 0;
        int iterations = 0;

        while(!processo.isEmpty()){
            iterations++;
            String currentName = processo.getFirst();
            int currentTimeLeft = tempo.getFirst();
            
            if (currentTimeLeft <= tempoInteracao){
                currentTime += currentTimeLeft;
                System.out.println(currentName + " "+ currentTime + " " + iterations);
                processo.removeFirst();
                tempo.removeFirst();
            } else {
                currentTime += tempoInteracao;
                tempo.removeFirst();
                tempo.addLast(currentTimeLeft- tempoInteracao);
                processo.rotate();
            }
        }

    }
    
}
