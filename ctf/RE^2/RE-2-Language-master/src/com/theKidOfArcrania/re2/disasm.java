/*
 * Copyright (c) 2017 theKidOfArcrania
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package com.theKidOfArcrania.re2;

import java.io.DataInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;

import static com.theKidOfArcrania.re2.MyUtils.*;

class disasm {
    public static final int REGISTER_COUNT = 0x10;
    public static final int REGISTER_MASK = REGISTER_COUNT - 1;
    public static final int SP = REGISTER_COUNT - 3;
    public static final int BP = REGISTER_COUNT - 2;
    public static final int IP = REGISTER_COUNT - 1;

    public static String regName(int idx){
        String s;
        switch (idx){
            case IP:
                s = "IP";
                break;

            case BP:
                s = "BP";
                break;

            case SP:
                s = "SP";
                break;

            default:
                s = "reg" + idx;
                break;
        }

        return s;
    }

    public static final int MAX_ADDR = 0xFFFF;

    public static short[] REGISTERS = new short[REGISTER_COUNT];
    public static byte[] MEMORY = new byte[MAX_ADDR + 1];

    public static Scanner in = new Scanner(System.in);
    public static short ipCache;
    public static short dis_ip = 0;

    public static HashMap<Integer, List<String>> opcode_table = new HashMap<>();

    public static void main(String[] args) throws Exception
    {
        opcode_table = loadOpcodeTxt();

        MEMORY = Files.readAllBytes(Paths.get("D:\\ctf\\only_code"));


        StringBuilder sb = new StringBuilder();
        while(dis_ip < MEMORY.length){
            int op = MEMORY[dis_ip] & 0xFF;
            sb.append(padLeft(hex(dis_ip), 8)).append(": ");
            dis_ip++;
            var a = opcode_table.getOrDefault(op, null);
            if(a == null){
                sb.append(padLeft("************* wrong opcode: ")).append(hex(op));
            }else{
                sb.append(padLeft(String.join(" ", a))).append(" ");
                step(op, sb);
            }
            System.out.println(sb.toString());
            sb.setLength(0);
        }
    }

    public static short readShort(DataInputStream dis) throws IOException
    {
        return getShort(dis.readByte(), dis.readByte());
    }

    public static byte indirectIncr(int variable)
    {
        byte val = MEMORY[dis_ip++];
        return val;
    }

    public static byte indirect(int register, int offset)
    {
        //pobierz cos z adresu [rejestr] + offset
        return 0;
    }

    public static short getShort(byte leastSig, byte mostSig)
    {
        int val = leastSig & 0xFF;
        val |= mostSig << 8;
        return (short)val;
    }

    public static void push(int val)
    {
    }

    public static short pop()
    {
        return 0;
    }

    public static void step(int opcode, StringBuilder sb)
    {
        short stmp;
        int itmp;
        String opt = "";

        switch (opcode)
        {
            case 0x3d: //PUSH [8-bit VALUE]
                opt += hex(indirectIncr(IP));
                break;
            case 0x4b: //PUSH [REG]
                opt += regName(indirectIncr(IP) & REGISTER_MASK);
                break;
            case 0x44: //PUSH [ADDR]
                int addr = getShort(indirectIncr(IP), indirectIncr(IP))
                        & MAX_ADDR;
                opt += hex(addr);
                break;
            case 0x4f: //POP [REG]
                itmp = indirectIncr(IP) & REGISTER_MASK;
                opt += regName(itmp);
                break;
            case 0x50: //PUSH [8-bit OFFSET]([REG])
                int var = indirectIncr(IP) & REGISTER_MASK;
                int off = indirectIncr(IP);
                opt += regName(var) + " " + hex(off);
                break;
            case 0x51: //PUSH ([REG])
            case 0x5f: //JMP ([REG])
            case 0x67: //STOREB ([REG])
            case 0x69: //STOREW ([REG])
            case 0x6b: //OUTPUTSTR ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                opt += regName(var);
                break;
            case 0x56: //STOREB [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                byte val = (byte)pop();
                opt += hex(addr) + " " + hex(val);
                break;
            case 0x57: //STOREW [ADDR]
            case 0x8e: //LOADB [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += hex(MEMORY[addr]);
                break;
            case 0x58: //JMP [ADDR]
            case 0x5a: //CALL [ADDR]
            case 0xda: //OUTPUTSTR [ADDR]
            case 0xff: //JP [ADDR]
            case 0xfe: //JN [ADDR]
            case 0xfc: //JZ [ADDR]
            case 0xde: //JNZ [ADDR]
                addr = getShort(indirectIncr(IP), indirectIncr(IP)) & MAX_ADDR;
                opt += hex(addr);
                break;
            case 0x63: //STOREW [8-bit OFFSET]([REG])
            case 0x64: //STOREB [8-bit OFFSET]([REG])
            case 0x65: //OUTPUTSTR [8-bit OFFSET]([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                off = indirectIncr(IP);
                opt += hex(off) + " " + regName(var);
                break;
            case 0x6a: //LOADW ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                stmp = getShort(indirect(var, 0), indirect(var, 1));
                opt += hex(stmp) + " " + regName(var);
                push(stmp);
                break;
            case 0x6c: //LOADB [8-bit OFFSET]([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                off = indirectIncr(IP);
                stmp = indirect(var, off);
                opt += hex(stmp) + " " + regName(var);
                break;
            case 0x6d: //EXIT [16-bit STATUSCODE]
                opt += hex(getShort(indirectIncr(IP), indirectIncr(IP)));
                break;
            case 0x6f: //PUSH [16-bit VALUE]
                stmp = getShort(indirectIncr(IP), indirectIncr(IP));
                opt += hex(stmp);
                break;
            case 0x7d: //CALL ([REG])
                var = indirectIncr(IP) & REGISTER_MASK;
                push(REGISTERS[IP]);
                opt += regName(var);
                break;
        }

        sb.append(opt);
    }

    private static void outputString(int addr)
    {
        int count = 0;
        while (MEMORY[addr + count] != 0)
            count++;
        byte[] output = new byte[count];
        System.arraycopy(MEMORY, addr, output, 0, count);
        System.out.print(new String(output));
    }
}
