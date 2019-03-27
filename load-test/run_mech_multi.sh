#!/bin/bash

set -x

for thr in 1 2 4 8 16 32
do
    echo "Running with ${thr} threads"
    sed -i "s/threads =.*$/threads = ${thr}/g" config.cfg
    ./run_mech.sh
done