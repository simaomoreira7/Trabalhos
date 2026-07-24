

public class BigNumber {

    private String value;

    public BigNumber(String n) {
        this.value = n;
    }
    
    public boolean equals(BigNumber n){
        return this.value.equals(n.value);
    }

    public String toString(){
        return value;
    }

    public BigNumber add(BigNumber n){
        
        String num1 = this.value;
        String num2 = n.value;

        StringBuilder result = new StringBuilder();

        int carry = 0;
        int i = num1.length();
        int j = num2.length();

        while ( i >= 0 || j >= 0 || carry > 0){
            int digit1 = 0;
            if ( i >= 0 ){
                digit1 = num1.charAt(i) - '0';
            }

            int digit2 = 0;
            if(j >= 0 ){
                digit2 = num2.charAt(j) - '0';
            }

            int sum = digit1 + digit2 + carry;

            carry = sum / 10;
            int currentDigit = sum %10;

            result.append(currentDigit);

            i--;
            j--;
        }

        String finalResult = result.reverse().toString();
        return new BigNumber (finalResult);
    }

    public BigNumber multiply(BigNumber n){
        String num1 = this.value;
        String num2 = n.value;

        if (num1.equals("0") || num2.equals("0")){
            return new BigNumber("0");
        }

        int len1 = num1.length();
        int len2 = num2.length();
        int[] result = new int[len1+len2];

        for (int i = len1 - 1; i >= 0; i--){
            for (int j = len2 - 1; j >= 0; j--){
                int digit1 = num1.charAt(i) - '0';
                int digit2 = num2.charAt(j) - '0';

                int product = digit1 * digit2;
                int pos1 = i + j;
                int pos2 = i + j + 1;

                int sum = product  + result[pos2];

                result[pos2] = sum % 10;
                result[pos1] += sum / 10;
            }
        }

        StringBuilder sb = new StringBuilder();
        for(int digit : result){
            if(!(sb.length() == 0 && digit == 0)){
                sb.append(digit);
            }
        }


        return new BigNumber(sb.toString());
    }

}



