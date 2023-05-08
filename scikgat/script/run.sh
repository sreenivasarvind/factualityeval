#!/bin/bash
#SBATCH --time=48:00:00
#SBATCH --gres=gpu
#SBATCH --qos=blanca-kann
#SBATCH --ntasks=1
#SBATCH --mem=32GB
#SBATCH --job-name=scikgat
#SBATCH --output=output/python-job.%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=arsr9646@colorado.edu
source /curc/sw/anaconda3/latest
conda activate /projects/arsr9646/is/multiversenv
python ./abstract_rerank/inference.py \
        -checkpoint ./model/abstract_scibert_mlm/pytorch_model.bin \
        -corpus ./data/kgat_corpus.jsonl \
        -abstract_retrieval ./prediction/abstract_retrieval_dev_top100.jsonl \
        -dataset ./data/kgat_test_claims.jsonl \
        -outpath ./prediction/abstract_rerank_dev_mlm.jsonl \
        -max_query_len 32 \
        -max_seq_len 256 \
        -batch_size 32 >console.txt
