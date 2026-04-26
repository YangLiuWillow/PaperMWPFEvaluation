#!/bin/bash
#SBATCH --job-name=speed-par-mwpf-color
#SBATCH --time=1-00:00:00
#SBATCH --mem=2G
#SBATCH --cpus-per-task=1
#SBATCH --partition=day
#SBATCH --output=slurm_job/speed-par-mwpf-color-%j.log
#SBATCH --error=slurm_job/speed-par-mwpf-color-%j.err

module purge
module load miniconda
conda activate par-mwpf

python capacity-color-par-mwpf.py
