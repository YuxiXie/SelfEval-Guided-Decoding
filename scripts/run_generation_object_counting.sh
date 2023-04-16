#!/bin/bash

set -x

split=test
dtname=object_counting

mkdir -p ${OUTPUTHOME}

cd ${EXEHOME}


python generate_code.py --verbal \
    --dt_name ${dtname} \
    --input_file ${DATAHOME}/${dtname}_${split}.jsonl \
    --output_dir ${OUTPUTHOME} \
    --use_mini_n --mini_n_samples 8 --max_tokens 128 \
    --sleep_time 20 \
    --reject_sample --bs_min_score 0.6 --unbiased \
    --bs_temperature 0.0 --bs_temperature_decay 0.5 \
    --temperature 0.0 --n_samples 16 --conf_ratio 0 
