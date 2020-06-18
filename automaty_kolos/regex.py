from xeger import Xeger
x = Xeger(limit=10)  # default limit = 10

reg = "a*b+a+(a|b)*"

w = set()
reg = reg.replace("*", "{0,3}").replace("+", "{1,3}")
print(reg)
i = 0
while len(w) < 30 and i < 1000:
    i += 1
    res = x.xeger(reg)
    w.add(res)

s = sorted(w)
for i in s:
    if not i:
        print("eps")
    else:
        print(i)

