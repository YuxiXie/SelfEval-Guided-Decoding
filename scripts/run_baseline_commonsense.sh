#!/bin/bash

set -x

split=train
dtname=csqa

mkdir -p ${OUTPUTHOME}

cd ${EXEHOME}

python generate_code_baseline.py --verbal \
    --chatgpt \
    --greedy \
    --dt_name ${dtname} \
    --input_file ${DATAHOME}/${dtname}_${split}.jsonl \
    --output_dir ${OUTPUTHOME} \
    --sleep_time 20 \
    --max_tokens 256

# --temperature 0.8 \
# --input_file ${DATAHOME}/gsm8k_${split}.jsonl \
# --n_samples 20 --use_mini_n --mini_n_samples 10
