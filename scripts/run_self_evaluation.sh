#!/bin/bash

set -x

split=test
dtname=gsm8k

cd ${EXEHOME}

python self_evaluate_code.py --verbal \
    --dt_name ${dtname} \
    --input_file ${DATAHOME}/${dtname}_sc_pal_tp0.2_s0_e1319_03_09_12_02.jsonl \
    --output_dir ${DATAHOME} \
    --use_mini_n 
