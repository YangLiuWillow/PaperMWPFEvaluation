#!/bin/bash

# Submit all par-mwpf benchmark jobs to slurm.
# Usage: bash submit_all_par_mwpf.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

submit() {
    local name="$1"
    local script="$2"
    local dir="$(dirname "$script")"

    sbatch <<EOF
#!/bin/bash
#SBATCH --job-name=${name}
#SBATCH --time=10:00:00
#SBATCH --mem=1G
#SBATCH --cpus-per-task=1
#SBATCH --partition=day
#SBATCH --output=${dir}/slurm_job/${name}-%j.log
#SBATCH --error=${dir}/slurm_job/${name}-%j.err

module purge
module load miniconda
conda activate par-mwpf

mkdir -p "${dir}/slurm_job"
cd "${dir}"
python "$(basename "$script")"
EOF

    echo "Submitted: ${name}"
}

# capacity-level noise models
submit "par-mwpf-depolarize" "${SCRIPT_DIR}/capacity-rsc/capacity-rsc-par-mwpf.py"
submit "par-mwpf-bias-x"    "${SCRIPT_DIR}/capacity-rsc/capacity-rsc-bias-x-par-mwpf.py"
submit "par-mwpf-bias-y"    "${SCRIPT_DIR}/capacity-rsc/capacity-rsc-bias-y-par-mwpf.py"
submit "par-mwpf-bias-y100" "${SCRIPT_DIR}/capacity-rsc/capacity-rsc-bias-y-eta100-par-mwpf.py"

# circuit-level noise
submit "par-mwpf-circuit"   "${SCRIPT_DIR}/circuit-rsc/circuit-rsc-par-mwpf.py"
