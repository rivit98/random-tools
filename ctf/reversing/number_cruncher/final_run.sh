if [ "$#" -ne 1 ]; then
    echo "run.sh data_file"
	exit
fi

g++ my_cruncher.cpp -DDEBUG --std=c++2a -o my_cruncher
# g++ my_cruncher.cpp --std=c++2a -o my_cruncher
./my_cruncher $1