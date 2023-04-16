## **Experiment Results**

#### **GSM8k (test - 1,319)**

| Models | Accuracy (%) | PS |
| :---- | :---------- | :- |
|| **Best Of (select 1)** |
| B1. PoT | 71.6 |
| B2. PAL | 72.0 |
| B3. PAL (chatGPT) | 78.7 |
| B4. CoT (chatGPT) | 80.8 |
| O1. Ours (t=0.5, t'=0.0) | 76.346 |
| O2. Ours (t=0.5, t'=0.05) | 77.255 |
| O3. Ours (t=0.5, t'=0.1) | 76.497 |
| O4. Ours (t=0.5, t'=0.2) | 75.512 |
| O5. Ours (t=0.5, t'=0.5) | 74.071 |
| O5'. Ours (t=0.5, t'=0.5, unbiased) | 74.526 |
| O6. Ours (t=0.5, t'=0.5(decay0.5)) | 77.786 / 79.833 / 77.862 / 79.075 / 77.407 / 78.772 / 77.862 / 78.469 / 79.076 |
| O6'. Ours (t=0.5, t'=0.5(decay0.5), unbiased) | 79.303 |
| O7. Ours (t=0.8, t'=0.0) | **80.061** |
| O8. Ours (t=0.8, t'=0.01) | 78.772 |
| O9. Ours (t=0.8, t'=0.4) | 71.342 |
| O10. Ours (t=0.8, t'=0.2(decay=0.5), unbiased) | 78.393 |
| O11. Ours (t=0.8, t'=0.8(decay=0.5), unbiased) | 76.649 |
| O12. Ours (t=0.8, t'=0.5(decay0.5)) | 77.255 / 76.270 / 76.497 / 77.483 / 76.876 / 76.422 / 77.028 / 76.876 / 77.786 / 77.693 / 76.194 / 76.876 / 77.635 |
| O12'. Ours (t=0.8, t'=0.5(decay0.5), unbiased) | 77.786 / 76.801 / 77.862 / 77.635 |
| O13. Ours (t=0.8, t'=0.5(decay=0.2), unbiased) | 76.725 |
| O14. Ours (t=0.8, t'=0.5(decay=0.8), unbiased) | 73.692 |
| O15. Ours (t=0.8, t'=0.5, unbiased) | 70.205 |
| O16. Ours (t=1.0, t'=0.0) | 78.999 |
| O17. Ours (t=1.0, t'=0.5(decay0.5)) | 75.057 |
| O18. Ours (t=0.1, t'=0.5(decay=0.5), unbiased) | 79.303 |
| O19. Ours (t=0.2, t'=0.5(decay=0.5), unbiased) | **80.136** |
| Ocot1. Ours-CoT (t=0.5, t'=0.0) | 68.916 / 69.143 / 70.053 |
|| **Majority Voting (MV)** |
| B1. PoT + MV (N=40) | 80.0 |
| B2. PAL + MV (N=40) | 80.4 |
| O2'. Ours + MV (B=5, N=40, t=0.5, t'=0.05) | [82.790, 82.487, 82.638, 82.183, 82.790] | (tree_size: 203) |
| O5'. Ours + MV (B=5, N=40, t=0.5, t'=0.5) | [82.942, 82.259, 81.956, 81.804, 82.411] | (tree_size: 203) |
| E1. O1 + O2 + O3 + O4 + O5 + O7 + O8 + O9 (N=40=8*5) | [83.927, 84.306, 84.079, 84.458, 83.472] | (sample within the beam, t''=0.5, 8 runs, 5 per run)  |
| E2. O7 + O8 + O9 + O10 (N=40=4*10) | [82.563, 82.411, 82.942, 82.866, 82.638] | (sample within the beam, t''=0.5) |
| E3. O1 + O2 + O3 + O4 + O5 (N=40=5*8) | [82.032, 82.259, 82.411, 82.563, 82.714] | (sample within the beam, t''=0.5) |
| E4. O1 + O2 + O3 + O4 + O5 + O6 + O7 + O8 + O9 + O10 (N=40=10*4) | [84.003, 84.230, 84.230, **84.685**, 84.155] | (sample within the beam, t''=0.5) |
| E5. O6(8runs) (N=40=8*5) | [82.563, 83.017, 82.866, 82.942, 82.638] | (sample within the beam, t''=0.5) |
| E*. O10(10runs) (N=40=10*4) | [84.615, **85.308**, 84.846, 85.129, 84.538] | (N=8*5 [84.079, 83.700, 83.776, 83.624, 84.003]) |
| Ecot. Ocot1(4runs) (N=20=4*5) | [79.606, 78.999, 79.378, 79.227, 79.378] |

#### **AQUA (test - 254)**

| Models | Accuracy (%) | PS |
| :---- | :---------- | :- |
|| **Best Of (select 1)** |
| PoT | 54.1 |
| PAL (chatGPT) | 54.7 |
| O1. Ours (t=0.2, t'=0.0) | 55.118 |
| O2. Ours (t=0.2, t'=0.2(decay0.5)) | 55.118 |
| O3. Ours (t=0.4, t'=0.2(decay0.5)) | 55.118 / 51.181 / 52.362 / 55.118 / 55.118 / **55.906** |
| O4. Ours (t=0.5, t'=0.2(decay0.5)) | 52.756 |
| O5. Ours (t=0.8, t'=0.2(decay0.5)) | 54.331 / 50.394 |
| O6. Ours (t=0.2, t'=0.0) | 54.331 | (not consider prob, i.e., s(y)=c(y)) |
| O7. Ours (t=0.5, t'=0.0) | 51.969 | (not consider prob, i.e., s(y)=c(y)) |
|| **Majority Voting (MV)** |
| PoT + MV (N=30) | 58.6 |
| E1. O1 + O6 + O7 (N=30=3*10) | [61.024, 59.055, 61.417, 61.417, 59.843] | (sample within the beam, t''=0.5) |
| E2. O1 + O2 + O3 + O4 + O5(2runs) (N=30=6*5) | [62.992, 61.811, 61.417, 63.386, 64.961] | (sample within the beam, t''=0.5) |
| E3. O1 + O2 + O3(5runs) + O4 + O5(2runs) (N=30=10*3) | [**66.535**, 64.961, 65.354, 63.386, 64.173] | (sample within the beam, t''=0.5) |
| E*. O3(10runs) (N=30=10*3) | <u>TODO</u> | (N=6*5: [61.811, 63.386, 64.173, 62.992, 62.205]) (sample within the beam, t''=0.5) |

#### **SVAMP (test - 1,000)**

| Models | Accuracy (%) | PS |
| :---- | :---------- | :---- |
|| **Best Of (select 1)** |
| PAL | 79.4 |
| PoT | 85.2 |
| PAL (chatGPT) | 84.1 |
| O1. Ours (t=0.5, t'=0.0) | **89.6** |
| O2. Ours (t=0.5, t'=0.5(decay0.5)) | 89.4 / <u>TODO</u> |
| O3. Ours (t=0.8, t'=0.0) | 88.4 |
| O4. Ours (t=0.8, t'=0.5(decay0.5)) | 88.5 |
|| **Majority Voting (MV)** |
| PAL + MV (N=) | - |
| PoT + MV (N=30) | 89.1 |
| E1. O1 + O2 + O3 + O4 (N=20=4*5) | [**90.3**, 90.0, 89.9, 90.0, 90.0] | (sample within the beam, t''=0.01) |
| E*. O2(10runs) (N=30=10*3) | <u>TODO</u> |

#### **ASDIV (a - 2,096)**

| Models | Accuracy (%) | PS |
| :---- | :---------- | :-- |
|| **Best Of (select 1)** |
| PAL | 79.6 |
| PAL (chatGPT) | 86.6 |
| O1. Ours (t=0.5, t'=0.0) | 84.828 |
| O2. Ours (t=0.5, t'=0.5(decay0.5)) | <u>TODO</u> |
| O3. Ours (t=0.8, t'=0.0) | **84.927** |
| O4. Ours (t=0.8, t'=0.5(decay0.5)) | <u>TODO</u> |
|| **Majority Voting (MV)** |
| PAL + MV (N=) | - |
| E1. O1 + O3 (N=30=2*15) | [85.592, **85.830**, 85.735, 85.543, 85.353] | (sample within the beam, t''=0.5) |

#### **TABMWP (test - 7,686)**

| Models | Accuracy (%) | PS |
| :---- | :---------- | :-- |
|| **Best Of (select 1)** |
| PoT | 73.2 |
| PAL (chatGPT) | 80.6 |
| O1. Ours (t=0.5, t'=0.0) | **79.105** | 78.8 (on 1k) |
| O2. Ours (t=0.5, t'=0.5(decay0.5)) | 77.283 / 77.505 |
| O3. Ours (t=0.8, t'=0.0) | 78.754 |
| O4. Ours (t=0.8, t'=0.5(decay0.5)) | 75.761 |
|| **Majority Voting (MV)** |
| PoT + MV (N=30) | 81.8 |
| E1. O1 + O2 + O3 (N=30=2*15) | [80.341, ] | (sample within the beam, t''=0.5) |

#### **FINQA (test - 1,147)**

| Models | Accuracy (%) | PS |
| :---- | :---------- | :-- |
|| **Best Of (select 1)** |
| PoT | 64.5 |
| O1. Ours (t=0.2, t'=0.0) | 54.403 |
| O2. Ours (t=0.4, t'=0.0) | 53.357 |
| O3. Ours (t=0.5, t'=0.0) | 54.926 |
| O4. Ours (t=0.8, t'=0.0) | 53.618 |
|| **Majority Voting (MV)** |
| PoT + MV (N=30) | 68.1 |
| E1. O1 + O3 + O4 (N=30=3*10) | [56.495, 56.408, 56.059, 56.669, 56.582] |


#### Date Understanding (test - 369)

| Models | Accuracy (%) | PS |
| :---- | :---------- | :-- |
|| **Best Of (select 1)** |
| CoT | 64.8 |
| PAL | 76.2 |
| PAL (chatGPT) | 70.7 |
| O1. Ours (t=0.5, t'=0.0) | **78.591** |
|| **Majority Voting (MV)** |
| CoT + MV (N=) | - |
| E1. | - |

#### CSQA (dev - 1,221)

| Models | Accuracy (%) | PS |
| :---- | :---------- | :-- |
|| **Best Of (select 1)** |
| CoT | 78.296 |
| CoT (chatGPT) | 75.594 |
| O1. Ours (t=0.5, t'=0.0) | 81.163 / 80.753 |
| O2. Ours (t=0.8, t'=0.0) | 80.098 / 80.181 |
|| **Majority Voting (MV)** |
| CoT + MV (N=) | - |
| E1. | <u>TODO</u> [] |

#### CSQA (train - 9,741)

| Models | Accuracy (%) | PS |
| :---- | :---------- | :-- |
|| **Best Of (select 1)** |
| CoT | 75.372 |
| CoT (chatGPT) | 72.867 |
| O1. Ours (t=0.5, t'=0.0) | 77.774 |
|| **Majority Voting (MV)** |
| CoT + MV (N=) | - |
| E1. | <u>TODO</u> [] |

#### StrategyQA (test - 9,741)

| Models | Accuracy (%) | PS |
| :---- | :---------- | :-- |
|| **Best Of (select 1)** |
| CoT | 74.891 |
| CoT (chatGPT) | 65.895 |
| O1. Ours (t=0.1, t'=0.0) | 75.240 |
| O2. Ours (t=0.1, t'=0.5(decay)) | 75.939 |
| O3. Ours (t=0.2, t'=0.0) | 74.934 |
| O4. Ours (t=0.2, t'=0.5(decay)) | 75.153 / 76.638 |
| O5. Ours (t=0.5, t'=0.0) | 71.834 / 72.314 |
| O6. Ours (t=0.8, t'=0.0) | 72.358 |
|| **Majority Voting (MV)** |
| CoT + MV (N=) | - |
| E1. | <u>TODO</u> [] |

#### Spotrs (test - 1,000)

| Models | Accuracy (%) | PS |
| :---- | :---------- | :-- |
|| **Best Of (select 1)** |
| CoT | 98.5 |
| CoT (chatGPT) | 95.9 |
|O1. Ours (t=0.5, t'=0.0) | 96.7 |
|| **Majority Voting (MV)** |
| CoT + MV (N=) | - |
| E1. | <u>TODO</u> [] |

