#!/bin/bash

EC_INVALID_ARGUMENT=2

if [ $# -lt 1 ]; then
    echo "Usage: $( basename $0 ) FILE"
    exit ${EC_INVALID_ARGUMENT}
fi

cat ${1} | \
awk -F',' 'NF>0 && NF<3 && !/;/ {print NR, $0}' | \
tee >( wc -l | grep 0 > /dev/null && [ $? -eq 0 ] && echo 'PASS!!' )
