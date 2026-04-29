#!/bin/bash
#SBATCH --job-name=speed-par-mwpf
#SBATCH --time=1-00:00:00
#SBATCH --mem=2G
#SBATCH --cpus-per-task=1
#SBATCH --partition=day
#SBATCH --output=slurm_job/speed-par-mwpf-%j.log
#SBATCH --error=slurm_job/speed-par-mwpf-%j.err

module purge
module load miniconda
conda activate par-mwpf

# mkdir -p slurm_job
# cd "$(dirname "$0")"
python capacity-rsc-par-mwpf.py

