# Running Scripts

Before running, please define `EXEHOME`, `OUTPUTHOME`, and `DATAHOME` accordingly in the script.
- _e.g._,
    ```sh
    EXEHOME=/home/username/SelfEval-Guided-Decoding/src
    DATAHOME=/home/username/SelfEval-Guided-Decoding/data
    OUTPUTHOME=/home/username/SelfEval-Guided-Decoding/outputs/${dtname}/${split}_outputs
    ```

We provide three types of example scripts as follows: (1) baseline running; (2) ours running; (3) LLM evaluating.

PS: please adjust the variables `dtname` and `split` to specify the dataset

## Baseline Running

- `arithmetic` reasoning -- [`run_baseline.sh`](run_baseline.sh)
    * main code: `src/generate_code_baseline.py`

- `symbolic` reasoning -- [`run_baseline_symbolic.sh`](run_baseline_symbolic.sh)
    * main code: `src/generate_code.py`

- `commonsense` reasoning -- [`run_baseline_commonsense.sh`](run_baseline_commonsense.sh)
    * main code: `src/self_evaluate_code.py`

## Ours Running

- `arithmetic` reasoning
    * `GSM8K`: [Ours (PAL)](run_generation_gsm8k.sh), [Ours (CoT)](run_generation_gsm8k_cot.sh)
    * `AQUA`: [Ours (PAL)](run_generation_aqua.sh)
    * `SVAMP`: [Ours (PAL)](run_generation_svamp.sh)
    * `ASDiv`: [Ours (PAL)](run_generation_asdiv.sh)
    * `TabMWP`: [Ours (PAL)](run_generation_tabmwp.sh)

- `symbolic` reasoning
    * `Date Understanding`: [Ours (PAL)](run_generation_date.sh)
    * `Object Counting`: [Ours (PAL)](run_generation_object_counting.sh)

- `commonsense` reasoning
    * `CSQA`: [Ours (CoT)](run_generation_csqa.sh)
    * `StrategyQA`: [Ours (CoT)](run_generation_strategyqa.sh)
    * `Sports Understanding`: [Ours (CoT)](run_generation_sports.sh)

## LLM Evaluation

Run [`run_self_evaluation.sh`](run_self_evaluation.sh)


