import sys
from utils.dataset import merge_parallel_results

merge_parallel_results(sys.argv[1], int(sys.argv[2]))
