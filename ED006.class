import java.util.Scanner;

public class ED005 {
    public static void main(String[] arg){
    
        Scanner scanner = new Scanner(System.in);
        
        int n = scanner.nextInt();
        scanner.nextLine();
        
        int count = 0;

    
        while (count < n){

            boolean falha = false;
            String frase = scanner.nextLine();
            String[] parts = frase.split(" ");
            MyStack <Integer> pilha = new LinkedListStack<>();

            for (int i = 0; i < parts.length; i++){
                if (!parts[i].equals("*") && !parts[i].equals("/") && !parts[i].equals("+") && !parts[i].equals("-") ){

                    int valor = Integer.parseInt(parts[i]);
                    pilha.push(valor);

                } else {


                    if (pilha.size() < 2){
                        falha = true;
                    }

                    else if ( parts[i].equals("*")){
                        int n1 = pilha.pop();
                        int n2 = pilha.pop();
                        pilha.push(n1*n2);
    
                    }else if ( parts[i].equals("+")){
                        int n1 = pilha.pop();
                        int n2 = pilha.pop();
                        pilha.push(n1+n2);

                    }else if (parts[i].equals("-")){
                        int n1 = pilha.pop();
                        int n2 = pilha.pop();
                        pilha.push(n2-n1);
                    
                    }else if ( parts[i].equals("/")){
                        int n1 = pilha.pop();
                        int n2 = pilha.pop();
                        if (n1 == 0){
                            falha = true;
                        }
                        pilha.push(n2/n1);
                    }

                }
               
            }


        if (pilha.size() != 1 || falha ){
                System.out.println("Expressao Incorrecta");
            } else{
                System.out.println(pilha.top());
            }    
            count++;
        }

    }
}



