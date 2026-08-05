import java.util.Scanner;
import java.util.PriorityQueue;
import java.util.Comparator;

class Comprador {
    String nome;
    int preco;
    
    Comprador(String nome, int preco) {
        this.nome = nome;
        this.preco = preco;
    }
}

class ED215 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // Fila de prioridade com comparador personalizado para maior preço primeiro
        PriorityQueue<Comprador> ofertas = new PriorityQueue<>(new Comparator<Comprador>() {
            @Override
            public int compare(Comprador c1, Comprador c2) {
                // Ordena por preço decrescente (maior primeiro)
                // Se preços iguais, mantém ordem de inserção não é especificado, mas não há empates
                return Integer.compare(c2.preco, c1.preco);
            }
        });
        
        int n = scanner.nextInt();
        scanner.nextLine(); // Consumir a quebra de linha
        
        // Processar cada evento
        for (int i = 0; i < n; i++) {
            String linha = scanner.nextLine().trim();
            
            if (linha.startsWith("OFERTA")) {
                String[] partes = linha.split(" ");
                String nome = partes[1];
                int preco = Integer.parseInt(partes[2]);
                
                // Adicionar à fila de prioridade
                ofertas.add(new Comprador(nome, preco));
            } 
            else if (linha.equals("VENDA")) {
                // Remover a melhor oferta (maior preço)
                Comprador melhor = ofertas.poll();
                // Imprimir o resultado da venda
                System.out.println(melhor.preco + " " + melhor.nome);
            }
        }
        
        scanner.close();
    }
}