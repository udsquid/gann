#!/bin/bash

EC_INVALID_ARGUMENT=2

if [ $# -lt 1 ]; then
    echo "Usage: $( basename $0 ) FILE"
    exit ${EC_INVALID_ARGUMENT}
fi

cat ${1} | awk -F',' -v OFS='\t' 'NF==3 {print $1, $2, $3}'
