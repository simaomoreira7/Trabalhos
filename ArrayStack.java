public class ArrayListIntSet implements IntSet {
   
   private int size;  
   private int elem[]; 
   
   ArrayListIntSet(int maxSize) {
      elem = new int[maxSize];
      size = 0;
   }

   public boolean add(int x) {
      if (!contains(x)) {
         if (size == elem.length){
            throw new RuntimeException("Maximum size of set reached");         
         }
         elem[size] =  x;
         size++;
         return true;
      }
      return false;
   }

   public boolean remove(int x) {
      if (contains(x)) {
         int pos = 0;
         while (elem[pos] != x) pos++;
         size--;
         elem[pos] = elem[size]; // Trocar ultimo elemento 
         return true;            // com o que se removeu
      }
      return false;
   }
   
   
   public boolean contains(int x) {
      for (int i=0; i<size; i++)
         if (elem[i] == x)
            return true;
      return false;
   }
   
   public void clear() {
      size = 0;
   }
   
   public int size() {
      return size;
   }

   @Override 
   public String toString() {
      String res = "{";
      for (int i=0; i<size; i++) {
         if (i>0) res += ",";
         res += elem[i];
      }
      res += "}";
      return res;
   }

   public boolean equals(IntSet s) {
      if (this.size() != s.size()) {
         return false;
      }
      
      for (int i = 1; i <= 1000; i++) {
         if (this.contains(i) != s.contains(i)) {
            return false;
         }
      }
      return true;
    }

   public ArrayListIntSet intersection(IntSet s) {
      ArrayListIntSet result = new ArrayListIntSet(size);
    
      for (int i = 1; i <= 1000; i++) {
         if (this.contains(i) && s.contains(i)) {
            result.add(i);
         }
      }
        return result;
    }
}