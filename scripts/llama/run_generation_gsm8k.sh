#!/bin/bash

set -x

split=test
dtname=gsm8k

mkdir -p ${OUTPUTHOME}

cd ${EXEHOME}

python generate_code_llama.py --verbal \
    --dt_name ${dtname} \
    --model_name meta-llama/Llama-2-13b-hf \
    --input_file ${DATAHOME}/${dtname}_${split}.jsonl \
    --output_dir ${OUTPUTHOME} \
    --mini_n_samples 2 --mini_n_samples_eval 2 --max_tokens 52 \
    --beam_size 5 \
    --reject_sample --unbiased \
    --bs_temperature 0.0 --bs_temperature_decay 0.5 \
    --temperature 0.5 --n_samples 2 --conf_ratio 0