#!/bin/bash

set -x

for thr in 48 32 16 8 4 2 1
do
    echo "Running with ${thr} threads"
    sed -i "s/threads =.*$/threads = ${thr}/g" config.cfg
    ./run_mech.sh
    sleep 5
done