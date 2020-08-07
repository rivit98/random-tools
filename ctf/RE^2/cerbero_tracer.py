from Pro.Core import *
from Pro.UI import *
from Pro.ccast import sbyte
import os, struct

REG_COUNT = 16


def regName(id):
    if id == 0xD:
        return "SP"

    if id == 0xE:
        return "BP"

    if id == 0xF:
        return "IP"

    return "R" + str(id)

def to_dw(args):
  return struct.unpack("<H", args)[0]

opcodes = {
    0x21: ("AND", 1),
    0x22: ("DUP", 1),
    0x25: ("MULT", 1),
    0x26: ("NOT", 1),
    0x2a: ("OR", 1),
    0x2b: ("SUB", 1),
    0x2d: ("MOD", 1),
    0x2f: ("DIV", 1),
    0x3c: ("SAR", 1),
    0x3d: ("PUSH [8-bit_VALUE]", 1 + 1),
    0x3e: ("SHL", 1),
    0x3f: ("SHR", 1),
    0x44: ("LOADW [ADDR]", 1 + 2),
    0x4b: ("PUSH [REG]", 1 + 1),
    0x4f: ("POP [REG]", 1 + 1),
    0x50: ("LOADW [8-bit_OFFSET] ([REG])", 1 + 1 + 1),
    0x51: ("LOADB ([REG])", 1 + 1),
    0x56: ("STOREB [ADDR]", 1 + 2),
    0x57: ("STOREW [ADDR]", 1 + 2),
    0x58: ("JMP [ADDR]", 1 + 2),
    0x5a: ("CALL [ADDR]", 1 + 2),
    0x5e: ("ADD", 1),
    0x5f: ("JMP ([REG])", 1 + 1),
    0x63: ("STOREW [8-bit_OFFSET] ([REG])", 1 + 1 + 1),
    0x64: ("STOREB [8-bit_OFFSET] ([REG])", 1 + 1 + 1),
    0x65: ("OUTPUTSTR [8-bit_OFFSET] ([REG])", 1 + 1 + 1),
    0x67: ("STOREB ([REG])", 1 + 1),
    0x69: ("STOREW ([REG])", 1 + 1),
    0x6a: ("LOADW ([REG])", 1 + 1),
    0x6b: ("OUTPUTSTR ([REG])", 1 + 1),
    0x6c: ("LOADB [8-bit_OFFSET] ([REG])", 1 + 1 + 1),
    0x6d: ("EXIT [16-bit_VALUE]", 1 + 2),
    0x6f: ("PUSH [16-bit_VALUE]", 1 + 2),
    0x7c: ("XOR", 1),
    0x7d: ("CALL ([REG])", 1 + 1),
    0x7e: ("RET", 1),
    0x8e: ("LOADB [ADDR]", 1 + 2),
    0xda: ("OUTPUTSTR [ADDR]", 1 + 2),
    0xdb: ("OUTPUTNUM", 1),
    0xdc: ("POP", 1),
    0xde: ("JNZ [ADDR]", 1 + 2),
    0xdf: ("INPUT", 1),
    0xfc: ("JZ [ADDR]", 1 + 2),
    0xfe: ("JN [ADDR]", 1 + 2),
    0xff: ("JP [ADDR]", 1 + 2),
}

def disassemble(code, regs):
    output = []
    ip = regs[0xF]
    current_instruction = code[ip]

    while current_instruction != 0:
        opcode_str, ip_increment = opcodes.get(current_instruction, ("wrong opcode", 1))

        if "[ADDR]" in opcode_str:
            val = to_dw(code[ip+1:ip+3])
            opcode_str = opcode_str.replace("[ADDR]", "{} ({})".format(hex(val), val))

        if "[16-bit_VALUE]" in opcode_str:
            val = to_dw(code[ip + 1:ip + 3])
            opcode_str = opcode_str.replace("[16-bit_VALUE]", "{} ({})".format(hex(val), val))

        if "([REG])" and "[8-bit_OFFSET]" in opcode_str:
            off = code[ip+2]
            reg = code[ip+1] & 0xF
            opcode_str = opcode_str.replace("[8-bit_OFFSET]", "")
            opcode_str = opcode_str.replace("[REG]", "{} + {}".format(regName(reg), hex(off)))

        if "[REG]" in opcode_str:
            val = code[ip+1] & 0xF
            opcode_str = opcode_str.replace("[REG]", "{}".format(regName(val)))

        if "[8-bit_OFFSET]" in opcode_str:
            val = code[ip+1]
            opcode_str = opcode_str.replace("[8-bit_OFFSET]", "{}".format(hex(val)))

        if "[8-bit_VALUE]" in opcode_str:
            val = code[ip+1]
            opcode_str = opcode_str.replace("[8-bit_VALUE]", "{}".format(hex(val)))

        if opcode_str == "wrong opcode":
            opcode_str += " ({})".format(hex(current_instruction))

        if "OUTPUTSTR" in opcode_str:
            mem_str = []
            addr = to_dw(code[ip + 1:ip + 3])
            while code[addr] != 0:
                mem_str.append(chr(code[addr]))
                addr += 1

            opcode_str += "   ; {}".format(''.join(mem_str).strip())


        output.append("{}: {}".format(hex(ip).upper(), opcode_str))

        ip += ip_increment
        current_instruction = code[ip]


    return '\n'.join(output)


STEP_VIEW_ID = 1
DISASM_VIEW_ID = 2
MEMORY_VIEW_ID = 3
REGISTERS_VIEW_ID = 4
STACK_VIEW_ID = 5

# the dump directory should have files with increasing number as name
# e.g.: 0, 1, 2, etc.
DBGDIR = r"D:\\ctf\\RE-2-Language-master\\RE-2-Language-master\\mem_dump"
BPX = -1


# logic to extract the instruction pointer from the dumps
# we use that as text in the Trace table and to go to a break point
def loadStepDescr(ud, steps):
    stepsdescr = []
    bpx_pos = -1
    for step in steps:
        with open(os.path.join(DBGDIR, str(step)), "rb") as f:
            f.seek((REG_COUNT - 1) * 2)
            ip = struct.unpack_from("<H", f.read(2), 0)[0]
            if bpx_pos == -1 and ip == BPX:
                bpx_pos = len(stepsdescr)
            stepsdescr.append("0x%04X" % (ip,))
    ud["stepsdescr"] = stepsdescr
    if bpx_pos != -1:
        ud["bpxpos"] = bpx_pos


prev_mem = [0 for _ in range(0x10000)]
prev_off = 0
prev_end = 0

def loadStep(cv, step, ud):
    global prev_mem
    global prev_off
    global prev_end

    with open(os.path.join(DBGDIR, str(step)), "rb") as f:
       dump = f.read()

    regs = struct.unpack_from("<" + ("H" * REG_COUNT), dump, 0)
    ud["regs"] = regs


    # set up regs table
    t = cv.getView(REGISTERS_VIEW_ID)
    labels = NTStringList()
    labels.append("Register")
    labels.append("Value")
    t.setColumnCount(2)
    t.setRowCount(REG_COUNT)
    t.setColumnLabels(labels)
    t.setColumnCWidth(0, 10)
    t.setColumnCWidth(1, 20)


    # set up memory
    h = cv.getView(MEMORY_VIEW_ID)
    mem = dump[REG_COUNT * 2:]
    ud["mem"] = mem
    h.setBytes(mem)


    if mem != prev_mem:
        newOffset = -1
        end = 0
        for i, b in enumerate(mem):
            if b != prev_mem[i]:
                if newOffset == -1:
                    newOffset = i
                end += 1

        h.setSelectedRange(newOffset, end)
        h.setCurrentOffset(max(0, min(newOffset - 0x60, 0xFFFF)))

        prev_off = newOffset
        prev_end = end
    else:
        h.setSelectedRange(prev_off, prev_end)
        h.setCurrentOffset(max(0, min(prev_off - 0x60, 0xFFFF)))

    prev_mem = mem


    # set up stack table
    stack = []
    sp = ud["regs"][0xD]
    stack_base = 0xFFEF
    while stack_base > sp:
        stack.append(struct.unpack("<H", mem[sp:sp+2])[0])
        sp += 2

    ud["cursp"] = ud["regs"][0xD]
    ud["stack"] = stack


    t = cv.getView(STACK_VIEW_ID)
    labels = NTStringList()
    labels.append("Stack address")
    labels.append("Value")
    t.setColumnCount(2)
    t.setRowCount(len(stack))
    t.setColumnLabels(labels)
    t.setColumnCWidth(0, 10)
    t.setColumnCWidth(1, 20)


    # set up disasm
    t = cv.getView(DISASM_VIEW_ID)
    disasm = disassemble(mem, regs)
    t.setText(disasm)


def tracerCallback(cv, ud, code, view, data):
    if code == pvnInit:
        # get steps
        steps = os.listdir(DBGDIR)
        steps = [int(e) for e in steps]
        steps = sorted(steps)
        ud["steps"] = steps
        loadStepDescr(ud, steps)
        # set up steps
        t = cv.getView(STEP_VIEW_ID)
        labels = NTStringList()
        labels.append("Trace")
        t.setColumnCount(1)
        t.setRowCount(len(steps))
        t.setColumnLabels(labels)
        t.setColumnCWidth(0, 10)
        # go to bpx if any
        if "bpxpos" in ud:
            bpxpos = ud["bpxpos"]
            t.setSelectedRow(bpxpos)
        return 1
    elif code == pvnGetTableRow:
        vid = view.id()
        if vid == STEP_VIEW_ID:
            data.setText(0, str(ud["stepsdescr"][data.row]))
        elif vid == REGISTERS_VIEW_ID:
            data.setText(0, regName(data.row))
            v = ud["regs"][data.row]
            data.setText(1, "0x%X (%d)" % (v, v))
            if data.row >= 13:
                data.setBgColor(0, ProColor_Special)
                data.setBgColor(1, ProColor_Special)
        elif vid == STACK_VIEW_ID:
            spaddr = ud["cursp"] + (data.row * 2)
            data.setText(0, "0x%04X" % (spaddr,))
            v = ud["stack"][data.row]
            data.setText(1, "0x%X (%d)" % (v, v))
    elif code == pvnRowSelected:
        vid = view.id()
        if vid == STEP_VIEW_ID:
            loadStep(cv, ud["steps"][data.row], ud)
    return 0


def tracerDlg():
    ctx = proContext()
    v = ctx.createView(ProView.Type_Custom, "Tracer")
    user_data = {}
    v.setup("<ui><hs><table id='1'/><vs><text id='2'/><hex id='3'/></vs><table id='4'/><table id='5'/></hs></ui>",
            tracerCallback, user_data)
    dlg = ctx.createDialog(v)
    dlg.show()


tracerDlg()