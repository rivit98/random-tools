#!/bin/bash
cp plik.hex kopia.hex
cp ascii.hex kopia_ascii.hex
hexdump -e '"%08.8_ax  "' -e' 4/1 "%02x " "  " 4/1 "%02x " "  "  4/1 "%02x " "  " 4/1 "%02x "  ' -e '" \n"' plik.memdump > plik.hex
hexdump -e '" |" 16/1 "%_p" "|\n"' plik.memdump > ascii.hex
clear
diff -U 6 kopia.hex plik.hex | colordiff | diff-highlight > diff_res1
cp diff_res2 diff_res2_old

if cmp -s kopia_ascii.hex ascii.hex; then
	echo "TAKIE SAME"
else
	diff -U 6 kopia_ascii.hex ascii.hex | colordiff | diff-highlight > diff_res2
fi

clear
paste diff_res1 diff_res2
