import java.util.Scanner;

class Matrix {
   int data[][]; 
   int rows;     
   int cols;     

    Matrix(int r, int c) {
      data = new int[r][c];
      rows = r;
      cols = c;
   }

    public void read(Scanner in) {
      for (int i=0; i<rows; i++)
         for (int j=0; j<cols; j++)
            data[i][j] = in.nextInt();
    }

   public String toString() {
      String ans = "";
      for (int i=0; i<rows; i++) {
         for (int j=0; j<cols; j++)
            ans += data[i][j] + " ";
         ans += "\n";
      }
      return ans;
   } 
   
   
    public static Matrix identity(int n){
        Matrix id = new Matrix(n, n);
        for(int i = 0; i < n; i++){
            for(int j = 0; j < n; j++){
                if (i == j){
                    id.data[i][i] = 1;
                } else {
                    id.data[i][j] = 0;
                }
            }
        }
        return id;
    }

    public Matrix transpose(){
        Matrix transpose = new Matrix(this.cols, this.rows);
        for (int i = 0; i < this.rows; i++){
            for (int j = 0; j < this.cols; j++){
                transpose.data[j][i] = this.data[i][j];
            }
        }
        return transpose;
    }
    
    public Matrix sum(Matrix m){
        Matrix soma = new Matrix(m.rows, m.cols);
        for (int i = 0; i < m.rows; i++){
            for (int j = 0; j < this.cols; j++){
                soma.data[i][j] = this.data[i][j] + m.data[i][j];
            }
        }
        return soma;
    }

    public Matrix multiply(Matrix m){
        Matrix multiply = new Matrix(this.rows, m.cols);
        for(int i = 0; i < this.rows; i++){
            for (int j = 0; j < m.cols; j++){
                int sum = 0;
                for (int k = 0; k < this.cols; k++){
                    sum += this.data[i][k] * m.data[k][j];
                } 
                multiply.data[i][j] = sum;
            }
        }
        return multiply;
    }
}


