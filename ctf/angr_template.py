import angr
import claripy

p = angr.Project("Recklinghausen")

key_bytes = [claripy.BVS("byte_{}".format(i), 8) for i in range(0x21)]
key_bytes_AST = claripy.Concat(*key_bytes)

state = p.factory.entry_state(args=['./Recklinghausen', key_bytes_AST])

for byte in key_bytes:
    state.solver.add(byte > 0x20, byte < 0x7f)

sm = p.factory.simulation_manager(state)

print(sm.explore(find=lambda x: b"CONGRATULATIONS" in x.posix.dumps(1)))

if len(sm.found) > 0:
    found = sm.found[0]
    print(found.solver.eval(key_bytes_AST, cast_to=bytes))
else:
    print("Nope")
