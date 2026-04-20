import os
import arguably
import multiprocessing

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

decoder_vec = ["par_mwpf(c=0)", "par_mwpf(c=1000)", "par_mwpf(c=1000,p=4)"]

p_d_vec = [
    ("0.48", [3, 5, 7, 9]),
    ("0.45", [3, 5, 7, 9]),
    ("0.4", [3, 5, 7, 9]),
    ("0.3", [3, 5, 7, 9]),
    ("0.2", [3, 5, 7, 9]),
    ("0.1", [3, 5, 7]),
    ("0.05", [3, 5, 7]),
    ("0.02", [3, 5, 7]),
    ("0.01", [3, 5]),
    ("0.005", [3]),
]

code_vec: list[str] = []
noise_vec: list[str] = []
for p, d_vec in p_d_vec:
    for d in d_vec:
        code_vec.append(f"css_rsc(d={d})")
        noise_vec.append(f"biased(p={p},basis=Y,eta=100)")


@arguably.command
def main(*, target_precision: float = 0.04):
    from qec_lego_bench.notebooks.pL_p_compare_decoders import (
        notebook_pL_p_compare_decoders,
    )

    notebook_pL_p_compare_decoders(
        notebook_filepath=notebook_filepath,
        code=code_vec,
        noise=noise_vec,
        decoder=decoder_vec,
        target_precision=target_precision,
        local_maximum_jobs=local_maximum_jobs - 1,
        max_shots=10_000_000,
        high_pL_threshold=1.0,  # special for biased-Y where the threshold is close to 50%
        slurm_cores_per_node=32,
        slurm_processes_per_node=1,
        slurm_mem_per_job=0.5,
        slurm_extra=dict(walltime="1-00:00:00", queue="day"),
    )


if __name__ == "__main__":
    arguably.run()
