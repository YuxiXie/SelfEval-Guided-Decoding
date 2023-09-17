#!/bin/bash

set -x


split=test
dtname=gsm8k

mkdir -p ${OUTPUTHOME}

cd ${EXEHOME}

python generate_code_baseline_llama.py --verbal \
    --model_name meta-llama/Llama-2-13b-hf \
    --dt_name ${dtname} \
    --input_file ${DATAHOME}/${dtname}_${split}.jsonl \
    --output_dir ${OUTPUTHOME} \
    --max_tokens 600 \
    --batch_size 1 \
    --temperature 0.4 \
    --mini_n_samples 2 --n_samples 10