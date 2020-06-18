import exrex

expected_f = lambda n: 2 ** n

regs = [
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	"",
	""
]





# s = sorted(w)
# for i in s:
# 	if not i:
# 		print("eps")
# 	else:
# 		print(i)

for n in [2,3,4,5]:
	maxlen = n
	w = set()
	for reg in regs:
		if not reg:
			continue

		reg = reg.replace("*", "{{0,{}}}".format(maxlen)).replace("+", "{{1,{}}}".format(maxlen))
		# print(reg)

		res = exrex.generate(reg, 1000)
		for r in res:
			if len(r) == maxlen:
				w.add(r)
	done = len(w)
	expe = expected_f(maxlen)
	print("len={}".format(maxlen))
	print("{} words".format(len(w)))
	print("{} expected\n".format(expected_f(maxlen)))

	if(done != expe):
		break