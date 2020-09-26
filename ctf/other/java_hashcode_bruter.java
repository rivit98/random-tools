import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

class IsItTheFlag {
    static List<Integer> weights = new ArrayList<>();
    static int notLower = 1471587914;
    static int lower    = 1472541258;

    public static boolean isFlag(String str) {
        return str.hashCode() == notLower && str.toLowerCase().hashCode() == lower;
    }

    public static void testString(String s, int w_idx, int hashcode_value){
        if(hashcode_value <= 0 || w_idx >= weights.size()){
            if(isFlag(s)){
                System.out.println(s);
            }
            return;
        }

        int i = 0;
        int rest = hashcode_value;
        int sub = weights.get(w_idx);
        if(hashcode_value / sub < 0x20){
            return;
        }

        while(rest > 0 && i < 127){
            rest = hashcode_value - (sub * i);

//            if(w_idx == 0){ //speedup first char
//                if(i > 47 && i < 53){
//                    testString(s + (char)i, w_idx+1, rest);
//                }
//            }
//            else if(i >= 32){
            if(i >= 0x20){
                testString(s + (char)i, w_idx+1, rest);
            }
            i++;
        }
    }

    public static void runner(){
        weights = Arrays.asList(28629151, 923521, 29791, 961, 31, 1);

        var initString = "";
        var initHashCode = notLower;
        if(initString.length() > 0){
            for(int i = 0; i < initString.length(); i++){
                int mult = initString.charAt(i);
                int sub = mult * weights.get(i);
                initHashCode -= sub;
            }
        }
        System.out.println("Init string: [" + initString + "] hashcode left: " + initHashCode);
        testString(initString, initString.length(), initHashCode);
    }

    public static void main(String[] args) {
        runner();

    }
}