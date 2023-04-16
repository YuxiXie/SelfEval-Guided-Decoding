#!/bin/bash

set -x

split=test
dtname=aqua

mkdir -p ${OUTPUTHOME}

cd ${EXEHOME}

python generate_code.py \
    --dt_name ${dtname} \
    --input_file ${DATAHOME}/${dtname}_${split}.jsonl \
    --output_dir ${OUTPUTHOME} \
    --use_mini_n --mini_n_samples 8 --max_tokens 256 \
    --sleep_time 5 \
    --reject_sample \
    --bs_temperature 0.2 --bs_temperature_decay 0.5 \
    --temperature 0.4 --n_samples 16 --conf_ratio 0
