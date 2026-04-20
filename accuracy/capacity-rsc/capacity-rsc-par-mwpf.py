import os
import arguably
import multiprocessing

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

# original decoders for comparison
# decoder_vec = ["fb(max_tree_size=0)", "fb", "mwpf(c=0)", "mwpf(c=50)"]
# add par-mwpf decoders with different partition counts
decoder_vec = ["par_mwpf(c=0)", "par_mwpf(c=50)", "par_mwpf(c=50,p=4)"]

p_d_vec = [
    ("0.4", [3, 5, 7, 9, 11, 13]),
    ("0.3", [3, 5, 7, 9, 11, 13]),
    ("0.2", [3, 5, 7, 9, 11, 13]),
    ("0.15", [3, 5, 7, 9, 11, 13]),
    ("0.14", [3, 5, 7, 9, 11, 13]),
    ("0.13", [3, 5, 7, 9, 11, 13]),
    ("0.12", [3, 5, 7, 9, 11, 13]),
    ("0.1", [3, 5, 7, 9, 11, 13]),
    ("0.05", [3, 5, 7, 9, 11, 13]),
    ("0.02", [3, 5, 7, 9, 11]),
    ("0.01", [3, 5, 7]),
    ("0.005", [3, 5]),
    ("0.002", [3]),
    ("0.001", [3]),
]

code_vec: list[str] = []
noise_vec: list[str] = []
for p, d_vec in p_d_vec:
    for d in d_vec:
        code_vec.append(f"css_rsc(d={d})")
        noise_vec.append(f"depolarize(p={p})")


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
        slurm_maximum_jobs=5,
        slurm_cores_per_node=32,
        slurm_processes_per_node=1,
        slurm_mem_per_job=0.5,
        slurm_extra=dict(walltime="1-00:00:00", queue="day"),
    )


if __name__ == "__main__":
    arguably.run()
