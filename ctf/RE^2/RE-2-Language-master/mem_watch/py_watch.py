from watchgod import watch
import os

os.system("touch plik.hex")
os.system("touch ascii.hex")
os.system("touch diff_res2")
for changes in watch('./plik.memdump'):
	os.system("./w.sh")