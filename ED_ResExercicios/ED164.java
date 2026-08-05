import java.util.*;

public class ED164 {
    public static void main(String[] args) {
        
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        scanner.nextLine();
        String palavra = scanner.nextLine();

        ArrayList<String> nomes = new ArrayList<>();
        nomes.add(palavra);

        while(n > 1){
            palavra = scanner.nextLine();
            if (!nomes.contains(palavra)){
                nomes.add(palavra);
            }
            n--;
        }

        System.out.println(nomes.size());


    }
}
