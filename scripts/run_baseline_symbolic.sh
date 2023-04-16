#!/bin/bash

set -x

split=test
dtname=date_understanding

mkdir -p ${OUTPUTHOME}

cd ${EXEHOME}

python generate_code_baseline.py \
    --chatgpt \
    --greedy \
    --dt_name ${dtname} \
    --input_file ${DATAHOME}/${dtname}_${split}.jsonl \
    --output_dir ${OUTPUTHOME} \
    --sleep_time 20 \
    --max_tokens 600

# --temperature 0.0
