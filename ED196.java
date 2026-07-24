public class ED195{
    public static boolean balanced(String s){

        int comprimento = s.length();
        boolean regular = true;
        int c = 0;
        
        MyStack<Character> pilha = new LinkedListStack<Character>(); 

        while(c < comprimento){

            if (s.charAt(c) == '[' || s.charAt(c) == '('){
                pilha.push(s.charAt(c));
            } else if (s.charAt(c) == ']' ){
                if (pilha.isEmpty()){
                    regular = false;
                    break;
                }
                if(pilha.top() == '[' && !pilha.isEmpty()){
                    pilha.pop();
                } else{
                    regular = false;
                    break;
                }
            } else if (s.charAt(c) == ')'){
                if (pilha.isEmpty()){
                    regular = false;
                    break;
                }
                if(pilha.top() == '(' && !pilha.isEmpty()){
                    pilha.pop();
                } else {
                    regular = false; 
                    break;
                }
            }

            c++;
                
        }

        return regular && pilha.isEmpty();
    }
}