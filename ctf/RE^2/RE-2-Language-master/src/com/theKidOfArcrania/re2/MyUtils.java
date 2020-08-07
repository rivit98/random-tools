package com.theKidOfArcrania.re2;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MyUtils {
    public static final int MAX_ADDR = 0xFFFF;
    private static byte[] old_mem = new byte[MAX_ADDR + 1];

    public static int UP_TO = MAX_ADDR;
    public static boolean checkArrays(byte[] a1, byte[] a2){
        for(int i = 0; i < UP_TO; i++){
            if(a1[i] != a2[i]){
                return true;
            }
        }
        return false;
    }

    public static int counter = 0;
    public static boolean cleaned = false;
    public static void dumpMemory(byte[] a){
//        if(!checkArrays(a, old_mem)){
//            return;
//        }

        String fname = formatName();
        savefile(fname, a);
        counter++;
    }

    public static String formatName(){
//        String fname = "mem_watch/plik";
        String fname = "mem_dump/";

        if(!cleaned){
            Arrays.stream(Objects.requireNonNull(new File(fname).listFiles())).forEach(File::delete);
            cleaned = true;
        }

        fname += counter;
        return fname;
    }

    public static void savefile(String fname, byte[] a){
        try (FileOutputStream fos = new FileOutputStream( fname)) {
            byte[] toSave = Arrays.copyOfRange(a, 0, UP_TO);
            ByteBuffer buffer = ByteBuffer.allocate(RESquared.REGISTERS.length * 2);
            buffer.order(ByteOrder.LITTLE_ENDIAN);
            buffer.asShortBuffer().put(RESquared.REGISTERS);
//            buffer.asShortBuffer().put(clean.REGISTERS);
            byte[] bytes = buffer.array();

            fos.write(bytes);
            fos.write(toSave);
            old_mem = toSave;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static HashMap<Integer, List<String>> loadOpcodeTxt(){
        HashMap<Integer, List<String>> opcode_table = new HashMap<>();
        ArrayList<String> list = new ArrayList<>();
        try{
            Scanner s = new Scanner(new File("D:\\ctf\\RE-2-Language-master\\REOpcodes.txt"));
            while (s.hasNextLine()){
                list.add(s.nextLine());
            }
            s.close();
        }catch (Exception e){
            e.printStackTrace();
        }

        for(var instr : list){
            var tokens = instr.split(" ");
            if(!tokens[0].startsWith("0")){
                continue;
            }
            opcode_table.putIfAbsent(Integer.decode(tokens[0]), Stream.of(tokens).skip(1).collect(Collectors.toList()));
        }
        return opcode_table;
    }

    public static String hex(int val){
        return "0x" + Integer.toHexString(val & 0xFFFF);
    }

    public static String padRight(String s) {
        return padRight(s, 25);
    }

    public static String padRight(String s, int n) {
        return String.format("%-" + n + "s", s);
    }

    public static String padLeft(String s) {
        int n = 32;
        return padLeft(s, n);
    }

    public static String padLeft(String s, int n) {
        return String.format("%" + n + "s", s);
    }

    public static void dumpStrings(byte[] MEMORY){
        StringBuilder sb = new StringBuilder();
        for(int i = 0x2036; i < 0x2100; i++){
            var c = (char)MEMORY[i];
            if(sb.length() == 0){
                sb.append(hex(i)).append(": ");
            }
            if(c != 0){
                sb.append(c);
            }else{
                System.out.println(sb.toString());
                sb.setLength(0);
            }
        }
        System.out.println(sb.toString());
    }

    public static void dumpBytes(byte[] MEMORY, int off){
        var l = new LinkedList<Integer>();
        for(int i = off; i < off + 0x100; i++){
            var c = (int)MEMORY[i];
            l.add(c);
        }
        System.out.println(hex(off) + " " + l);
    }
}
