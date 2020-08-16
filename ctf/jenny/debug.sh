#!/bin/bash


# sudo gdb -ex "break Java_Jenny_verify" -ex "c" -p $(jps | grep "Jenny" | awk '{print $1}')
sudo gdb -ex "break *Java_Jenny_verify+509" -ex "c" -p $(jps | grep "Jenny" | awk '{print $1}')