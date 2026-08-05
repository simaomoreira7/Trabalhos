public class BooleanArrayIntSet implements IntSet {
    private boolean[] elements;
    private int currentSize;
    
    public BooleanArrayIntSet(int n) {
        // Criar array de booleanos para números no intervalo [1, n]
        this.elements = new boolean[n + 1]; // +1 porque os índices começam em 0, mas queremos 1..n
        this.currentSize = 0;
    }
    
    public boolean contains(int x) {
        // Verifica se x está dentro dos limites válidos
        if (x < 1 || x >= elements.length) {
            return false;
        }
        return elements[x];
    }
    
    public boolean add(int x) {
        // Verifica se x está dentro dos limites válidos
        if (x < 1 || x >= elements.length) {
            return false;
        }
        
        if (!elements[x]) {
            elements[x] = true;
            currentSize++;
            return true;
        }
        return false;
    }
    
    public boolean remove(int x) {
        // Verifica se x está dentro dos limites válidos
        if (x < 1 || x >= elements.length) {
            return false;
        }
        
        if (elements[x]) {
            elements[x] = false;
            currentSize--;
            return true;
        }
        return false;
    }
    
    public int size() {
        return currentSize;
    }
    
    public void clear() {
        // Preenche todo o array com false
        for (int i = 1; i < elements.length; i++) {
            elements[i] = false;
        }
        currentSize = 0;
    }
    
    public boolean equals(IntSet s) {
        if (this.size() != s.size()) {
            return false;
        }
        
        // Verifica se todos os elementos deste conjunto estão no outro
        for (int i = 1; i < elements.length; i++) {
            if (elements[i] && !s.contains(i)) {
                return false;
            }
        }
        return true;
    }
    
    public IntSet intersection(IntSet s) {
        // Cria um novo conjunto para a interseção
        BooleanArrayIntSet intersection = new BooleanArrayIntSet(elements.length - 1);
        
        // Adiciona apenas os elementos que estão em ambos os conjuntos
        for (int i = 1; i < elements.length; i++) {
            if (elements[i] && s.contains(i)) {
                intersection.elements[i] = true;
                intersection.currentSize++;
            }
        }
        return intersection;
    }
}