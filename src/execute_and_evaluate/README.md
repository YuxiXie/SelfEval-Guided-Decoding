# Post-Processing and Evaluating

PS: Please adjust the argument to `sys.path.append()` accordingly.

## Baseline Outputs

```sh
baseline_interpret_and_evaluate.py
```
Required argument: path to the output file for evaluation.

## Ours Outputs

```sh
interpret_and_evaluate.py
```
Required argument: path to the output file for evaluation.

```sh
interpret_and_evaluate_ensemble.py
```
Please adjust `N` and `filenames` for majority voting.

## AQUA Outputs

```sh
aqua_interpret_and_evaluate.py
aqua_interpret_and_evaluate_ensemble.py
```
Since AQUA requires to select from several choices according to the reasoning result, an addtional step of prompting is required to conduct the selection.
Therefore, we have separate scripts to post-process the outputs.

