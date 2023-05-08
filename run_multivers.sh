#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:a40
#SBATCH --qos=preemptable
#SBATCH --ntasks=1
#SBATCH --mem=32GB
#SBATCH --job-name=multivers
#SBATCH --output=output/python-job.%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=arsr9646@colorado.edu
source /curc/sw/anaconda3/latest
conda activate /projects/arsr9646/is/multivers/projects/arsr9646/is/envmultivers
python multivers/predict.py \
        --checkpoint_path=checkpoints/scifact.ckpt \
        --input_file=data/test_claims.jsonl \
        --corpus_file=data/corpus.jsonl \
        --output_file=data/output.jsonl > multivers_console.txt
