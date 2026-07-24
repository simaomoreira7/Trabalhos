import java.util.*;

public class ED172 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        BSTMap<String, Integer> dicionario = new BSTMap<>();
        
        while (scanner.hasNext()) {
            String palavra = scanner.next();
            
            Integer contador = dicionario.get(palavra);
            
            if (contador == null) {
                dicionario.put(palavra, 1);
            } else {
                dicionario.put(palavra, contador + 1);
            }
        }
        
        LinkedList<String> palavras = dicionario.keys();
        

        for (String palavra : palavras) {
            System.out.println(palavra + ": " + dicionario.get(palavra));
        }
        
        scanner.close();
    }
}
