#!/bin/bash


cp $1{,.bak}
xxd -g8 $1 | sed -r s/725f76312e34[3-9][1-9]5d/725f76312e34305d/ | xxd -r > $1
#mv .temp.binary $1
#rm -f .temp.binary
