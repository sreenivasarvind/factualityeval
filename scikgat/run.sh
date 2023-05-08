#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --qos=preemptable
#SBATCH --gres=gpu:a100
#SBATCH --ntasks=1
#SBATCH --mem=64GB
#SBATCH --job-name=scikgat
#SBATCH --output=output/python-job.%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=arsr9646@colorado.edu
source /curc/sw/anaconda3/latest
conda activate /projects/arsr9646/is/multiversenv
export TRANSFORMERS_CACHE='/projects/arsr9646/huggingface'
export PIP_CACHE_DIR='/projects/arsr9646/pip'
python kgat/test.py --outdir ./prediction \
 --corpus data/kgat_corpus.jsonl \
 --evidence_retrieval prediction/rationale_selection_dev_scibert_mlm_try.jsonl \
 --dataset data/kgat_test_claims.jsonl \
 --checkpoint model/kgat_roberta_large_mlm/model.best.pt \
 --pretrain mlm_model/roberta_large_mlm \
 --name kgat_dev_roberta_large_mlm.json \
 --roberta \
 --bert_hidden_dim 1024
