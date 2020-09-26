package com.theKidOfArcrania.re2;

import java.io.DataInputStream;
import java.io.EOFException;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.*;

import static com.theKidOfArcrania.re2.MyUtils.*;
import static com.theKidOfArcrania.re2.disasm.regName;

public class RESquared {

    public static final int REGISTER_COUNT = 0x10;
    public static final int REGISTER_MASK = REGISTER_COUNT - 1;
    public static final int SP = REGISTER_COUNT - 3;
    public static final int BP = REGISTER_COUNT - 2;
    public static final int IP = REGISTER_COUNT - 1;

    public static final byte[] SIGNATURE = {0x52, 0x45, 0x5e, 0x32, 0x00, 0x00, 0x00, 0x01}; //RE^2

    public static final int MAX_ADDR = 0xFFFF;
    public static final int STACK_ADDR = 0xFFF0;

    public static short[] REGISTERS = new short[REGISTER_COUNT];
    public static byte[] MEMORY = new byte[MAX_ADDR + 1];

    public static Scanner in = new Scanner(System.in);
    public static short ipCache;

    public static HashMap<Integer, List<String>> opcode_table = new HashMap<>();
    static int stack_bottom = STACK_ADDR;

    public static void main(String[] args) {
        opcode_table = loadOpcodeTxt();

        String file = args[0];
        System.out.println();
        try (DataInputStream dis = new DataInputStream(new FileInputStream(file)))
        {
            byte[] sig = new byte[SIGNATURE.length];
            dis.readFully(sig);
            if (!Arrays.equals(SIGNATURE, sig))
                throw new Exception();

            REGISTERS[IP] = readShort(dis); //entry point
            System.out.println("Entry point: " + hex(REGISTERS[IP]));
            byte sections = dis.readByte();
            if (sections < 0)
                throw new Exception();

            for (int i = 0; i < sections; i++)
            {
                int offset = readShort(dis) & MAX_ADDR;
                short size = readShort(dis);
                if (size < 0)
                    throw new Exception();

                dis.readFully(MEMORY, offset, size);
            }

            REGISTERS[BP] = REGISTERS[SP] = (short)STACK_ADDR;

            while (true)
                step();
        }
        catch (EOFException e)
        {
            System.out.println("ERROR: Binary format error.");
            System.exit(1);
        }
        catch (IOException e)
        {
            System.out.println("ERROR: File not found: " + file);
            System.exit(1);
        }
        catch (IndexOutOfBoundsException e)
        {
            System.out.println("ERROR: Segmentation Fault.");
            //e.printStackTrace();
            System.exit(3);
        }
        catch (Exception e)
        {
            System.out.println("ERROR: Binary format error.");
            System.out.println(e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }

    }

    public static short readShort(DataInputStream dis) throws IOException
    {
        return getShort(dis.readByte(), dis.readByte());
    }

    public static byte indirectIncr(int variable)
    {
        byte val = MEMORY[REGISTERS[variable] & MAX_ADDR];
        REGISTERS[variable]++;
        return val;
    }

    public static byte indirect(int variable, int offset)
    {
        byte val = MEMORY[((variable == IP ? ipCache : REGISTERS[variable]) &
                MAX_ADDR) + offset];
        return val;
    }

    public static short getShort(byte leastSig, byte mostSig)
    {
        int val = leastSig & 0xFF;
        val |= mostSig << 8;
        return (short)val;
    }

    public static void putIndirect(byte val, int variable, int offset)
    {
        int offff = ((variable == IP ? ipCache : REGISTERS[variable]) & MAX_ADDR) + offset;
        MEMORY[offff] = val;
    }

    public static void putShort(short val, int addr)
    {
        MEMORY[addr] = (byte)val;
        MEMORY[addr + 1] = (byte)(val >> 8);
    }

    public static void putShortIndirect(short val, int variable, int offset)
    {
        putShort(val, ((variable == IP ? ipCache : REGISTERS[variable]) &
                MAX_ADDR) + offset);
    }

    public static void push(int val)
    {
        REGISTERS[SP] -= 2;
        putShortIndirect((short)val, SP, 0);

    }

    public static short pop()
    {
        REGISTERS[SP] += 2;
        short res = getShort(indirect(SP, -2), indirect(SP, -1));
        return res;
    }

    public static short fake_pop()
    {
        REGISTERS[SP] += 2;
        short res = getShort(indirect(SP, -2), indirect(SP, -1));
        REGISTERS[SP] -= 2;
        return res;
    }

    public static         boolean startDump = false;

    public static void step()
    {
        ipCache = REGISTERS[IP];
        int opcode = indirectIncr(IP) & 0xff;

        short stmp;
        int itmp;
        String asdf = String.join(" ", opcode_table.getOrDefault(opcode, Collections.singletonList("NIC")));
        String opt = padLeft(hex(REGISTERS[IP] - 1 - 0x8000), 6) + ": " + padLeft(asdf) + " ";
        if(hex(REGISTERS[IP] - 1 - 0x8000).equals("0x10e")){
            startDump = true;
        }

        switch (opcode)
        {
            case 0x21: //AND
                opt += hex(fake_pop()) + " & " + hex(fake_pop());
                push(pop() & pop());
                break;
            case 0x22: //DUP
                stmp = getShort(indirect(SP, 0), indirect(SP, 1));
                opt += hex(stmp);
                push(stmp);
                break;
            case 0x25: //MULT
                opt += hex(fake_pop()) + " * " + hex(fake_pop());
                push(pop() * pop());
                break;
            case 0x26: //NOT
                opt += hex(fake_pop()) + " --> " + hex(~fake_pop());
                push(~pop());
                break;
            case 0x2a: //OR
                stmp = pop();
                opt += hex(stmp) + " | " + hex(fake_pop());
                push(stmp | pop());
                break;
            case 0x2b: //SUB
                int tmp = pop();
                opt += hex(fake_pop()) + " - " + hex(tmp);
                push(pop() - tmp);
                break;
            case 0x2d: //MOD
                tmp = pop();
                opt += hex(fake_pop()) + " % " + hex(tmp);
                push(pop() % tmp);
                break;
            case 0x2f: //DIV
                tmp = pop();
                opt += hex(fake_pop()) + " / " + hex(tmp);
                push(pop() / tmp);
                break;
            case 0x3c: //SAR
                tmp = pop();
                opt += hex(fake_pop()) + " >> " + hex(tmp);
                push(pop() >> tmp);
                break;
            case 0x3d: //PUSH [8-bit VALUE]
                stmp = indirectIncr(IP);
                opt += hex(stmp);
                push(stmp);
                break;
            case 0x3e: //SHL
                tmp = pop();
                opt += hex(fake_pop()) + " << " + hex(tmp);
                push(pop() << tmp);
                break;
            case 0x3f: //SHR
                tmp = pop();
                opt += hex(fake_pop()) + " " + hex(tmp);
                push((pop() & 0xFFFF) >>> tmp);
                break;
            case 0x44: //PUSH [ADDR]
                int addr = getShort(indirectIncr(IP), indirectIncr(IP))
                        & MAX_ADDR;
                stmp = getShort(MEMORY[addr], MEMORY[addr + 1]);
                opt += hex(stmp) + " from addr " + hex(addr);
                push(stmp);
                break;
            case 0x4b: //PUSH [REG]
                int stm2 = indirectIncr(IP) & REGISTER_MASK;
                itmp = REGISTERS[stm2];
                opt += hex((short)itmp) + " from " + regName(stm2);
                push(itmp);
                break;
            case 0x4f: //POP [REG]
                itmp = indirectIncr(IP) & REGISTER_MASK;
                opt += regName(itmp) + " <--- " + hex(fake_pop());
                REGISTERS[itmp] = pop();
                break;
            case 0x50: //PUSH/LOADW [8-bit OFFSET]([REG])
                int var = indirectIncr(IP) & REGISTER_MASK;
                int off = indirectIncr(IP);
                opt += regName(var) + " + " + hex(off) + " (" + hex(getShort(indirect(var, off), indirect(var, off + 1))) + ")";
                push(getShort(indirect(var, off), indirect(var, off + 1)));
                break;
            case 0x51: //LOADB ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                stmp = indirect(var, 0);
                opt += "from " + regName(var) + " val: " + hex(stmp);
                push(stmp);
                break;
            case 0x56: //STOREB [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                byte val = (byte)pop();
                opt += hex(addr) + " = " + hex(val);
                MEMORY[addr] = val;
                System.out.println(padLeft("store " + hex(val) + " (" + val + ") at " + hex(addr), 100));

                break;
            case 0x57: //STOREW [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += hex(addr) + " = " + hex(fake_pop());
                putShort(pop(), addr);
                break;
            case 0x58: //JMP [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += hex(addr);
                REGISTERS[IP] = (short)addr;
                break;
            case 0x5a: //CALL [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += hex(addr) + " (PUSH " + hex(REGISTERS[IP]) + ")";
                push(REGISTERS[IP]);
                REGISTERS[IP] = (short)addr;
                break;
            case 0x5e: //ADD
                stmp = pop();
                opt += hex(stmp) + " + " + hex(fake_pop());
                push(stmp + pop());
                break;
            case 0x5f: //JMP ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                stmp = getShort(indirect(var, 0), indirect(var, 1));
                opt += hex(stmp) + " from " + regName(var);
                REGISTERS[IP] = stmp;
                break;
            case 0x63: //STOREW [8-bit OFFSET]([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                off = indirectIncr(IP);
                opt += hex(fake_pop()) + " into " + regName(var) + " + " + hex(off);
                putShortIndirect(pop(), var, off);
                break;
            case 0x64: //STOREB [8-bit OFFSET]([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                off = indirectIncr(IP);
                opt += hex((byte)fake_pop()) + " into " + regName(var) + " + off: " + hex(off);
                putIndirect((byte)pop(), var, off);
                break;
            case 0x65: //OUTPUTSTR [8-bit OFFSET]([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                off = indirectIncr(IP);
                opt += regName(var) + " off: " + hex(off) + " target: " + hex((var == IP ? ipCache : REGISTERS[var]) + off
                        & MAX_ADDR);
                outputString(((var == IP ? ipCache : REGISTERS[var]) + off)
                        & MAX_ADDR);
                break;
            case 0x67: //STOREB ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                opt += "[" + regName(var) + "] <--- " + hex((byte)fake_pop());
                putIndirect((byte)pop(), var, 0);
                break;
            case 0x69: //STOREW ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                opt += regName(var) + " <--- " + hex(fake_pop());
                putShortIndirect(pop(), var, 0);
                break;
            case 0x6a: //LOADW ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                stmp = getShort(indirect(var, 0), indirect(var, 1));
                opt += hex(stmp) + " from " + regName(var);
                push(stmp);
                break;
            case 0x6b: //OUTPUTSTR ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                opt += regName((var == IP ? ipCache : REGISTERS[var]) & MAX_ADDR);
                outputString((var == IP ? ipCache : REGISTERS[var]) & MAX_ADDR);
                break;
            case 0x6c: //LOADB [8-bit OFFSET]([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                off = indirectIncr(IP);
                stmp = indirect(var, off);
                opt += hex(stmp) + " from " + regName(var) + " off: " + hex(off);
                push(stmp);
                break;
            case 0x6d: //EXIT [16-bit STATUSCODE]
                opt += hex(getShort(indirectIncr(IP), indirectIncr(IP)));
                System.exit(getShort(indirectIncr(IP), indirectIncr(IP)));
                break;
            case 0x6f: //PUSH [16-bit VALUE]
                stmp = getShort(indirectIncr(IP), indirectIncr(IP));
                opt += hex(stmp);
                push(stmp);
                break;
            case 0x7c: //XOR
                stmp = pop();
                opt += hex(stmp) + " ^ " + hex(fake_pop());
                push(stmp ^ pop());
                break;
            case 0x7d: //CALL ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                push(REGISTERS[IP]);
                stmp = getShort(indirect(var, 0), indirect(var, 1));
                opt += hex(stmp) + " from reg: " + regName(var) + " (PUSH " +  hex(REGISTERS[IP]) + ")";
                REGISTERS[IP] = stmp;
                break;
            case 0x7e: //RET
                opt += hex(fake_pop());
                REGISTERS[IP] = pop();
                break;
            case 0x8e: //LOADB [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += "addr: " + hex(addr) + " (" + hex(MEMORY[addr]) + ")";
                push(MEMORY[addr]);
                break;
            case 0xda: //OUTPUTSTR [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += hex(addr);
                outputString(addr);
                break;
            case 0xdb: //OUTPUTNUM
                opt += hex(fake_pop());
                System.out.print(pop());
                break;
            case 0xdc: //POP
                opt += hex(fake_pop());
                pop();
                break;
            case 0xde: //JNZ [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += "if " + hex(fake_pop()) + " != 0 then jmp to " + hex(addr);
                if (pop() != 0){
                    REGISTERS[IP] = (short)addr;
                }
                break;
            case 0xdf: //INPUT
                try
                {
                    if(inputIdx >= inputValues.length){
                        push(in.nextShort());
                    }else{
                        push(inputValues[inputIdx++]);
                    }
                }
                catch (Exception e)
                {
                    System.out.println("ERROR: Invalid number entered.");
                    System.exit(4);
                }
                break;
            case 0xfc: //JZ [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += "if " + hex(fake_pop()) + " == 0 then jmp to " + hex(addr);
                if (pop() == 0){
                    REGISTERS[IP] = (short)addr;
                }
                break;
            case 0xfe: //JN [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += "if " + hex(fake_pop()) + " < 0 then jmp to " + hex(addr);
                if (pop() < 0){
                    REGISTERS[IP] = (short)addr;
                }
                break;
            case 0xff: //JP [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += "if " + fake_pop() + " [" + hex(fake_pop()) + "] > 0 then jmp to " + hex(addr);
                if (pop() > 0){
                    REGISTERS[IP] = (short)addr;
                }
                break;
            default:
                System.out.printf("ERROR: Invalid opcode: 0x%02x\n@0x%04x",
                        opcode, Short.toUnsignedInt(ipCache));
                System.exit(1);
                break;
        }

        List<String> stack_contents = new ArrayList<>();
        List<String> registers_contents = new ArrayList<>();
        for(int i = 0; i < 0x10 - 3 - 6 - 1; i++){
            registers_contents.add(hex(REGISTERS[i]));
        }

        for(int i = stack_bottom; i > (REGISTERS[SP] & 0xFFFF); i -= 2){
//        for(int i = STACK_ADDR + 1; i > (REGISTERS[SP] & 0xFFFF); i -= 2){
//            System.out.println(hex(getShort(MEMORY[i], MEMORY[i-1])));
            var a = getShort(MEMORY[i-1], MEMORY[i]);
//            var a = getShort(MEMORY[i], MEMORY[i-1]);
            stack_contents.add(hex(a));
        }
        opt = padRight(padLeft(opt, 32), 81);
        if(inputIdx >= inputValues.length && startDump){
//            System.out.println(opt + " " + stack_contents);
            System.out.println(opt + " " + stack_contents + "          Regs: " + registers_contents);
            dumpMemory(MEMORY);
        }
    }

    public static int inputIdx = 0;
    public static short[] inputValues = {0x325e, 0x2121,
            0, 0x10};
    private static void outputString(int addr)
    {
        int count = 0;
        while (MEMORY[addr + count] != 0)
            count++;
        byte[] output = new byte[count];
        System.arraycopy(MEMORY, addr, output, 0, count);
        System.out.print(new String(output));
        System.out.println();
    }
}