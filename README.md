# SelfEval-Guided Decoding for Multi-step Reasoning

We endow Large Language Models (LLMs) with fine-grained self-evaluation to refine multi-step reasoning inference. 
We propose an effective prompting approach that integrates self-evaluation guidance through stochastic beam search. 
Our approach explores the reasoning search space using a well-calibrated automatic criterion. 
This enables an efficient search to produce higher-quality final predictions. 
With the self-evaluation guided stochastic beam search, we also balance the quality–diversity trade-off in the generation of reasoning chains. 
This allows our approach to adapt well with majority voting and surpass the corresponding Codex-backboned baselines by $6.34$%, $9.56$%, and $5.46$% on the GSM8K, AQUA, and StrategyQA benchmarks, respectively, in few-shot accuracy. 
Analysis of our decompositional reasoning finds it pinpoints logic failures and leads to higher consistency and robustness. 

![Model Framework](analysis/framework-prompt.png)

## Requirements

#### Environment

```
openai                             0.27.1
matplotlib                         3.3.4
numpy                              1.20.1
ipdb                               0.13.9
tqdm                               4.64.1
```

#### Data Preprocessing

We provide example formats of the input dataset in the folder [`data`](data).
For other datasets, please check the details about [prompt construction](src/utils/prompt.py) to know the specific attributes each data point should contain.

#### OpenAI Keys

In the current version of our main method (in [`generate_code.py`](src/generate_code.py)), we adopt [`Codex`](https://openai.com/blog/openai-codex) as our backend LLM.
However, OpenAI has discontinued public access to this model.
To address this, you can either 1) apply for the [research access](https://openai.com/form/researcher-access-program) to `Codex` (`code-davinci-002`) to run our approach, or 2) utilize an alternative backbone `text-davinci-003`.
We will later also release the results of running based on `text-davinci` models for reference.


## Running

We show examples of how to run our method on different datasets in [`scripts`](scripts), like [the script for gsm8k](scripts/run_generation_gsm8k.sh).


---
<sub><sup>[crt] This repository is adapted from the code of the works [PaL: Program-Aided Language Model](https://github.com/reasoning-machines/pal) and [Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks](https://github.com/wenhuchen/Program-of-Thoughts). </sup></sub>


