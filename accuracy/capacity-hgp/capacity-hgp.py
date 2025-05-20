import os
import arguably
import multiprocessing

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"


decoder_vec = ["mwpf(c=0)", "mwpf(c=200)", "bposd(max_iter=4,ms_scaling_factor=0.3)"]
p_vec = [
    "0.2",
    "0.1",
    "0.05",
    "0.04",
    "0.03",
    "0.025",
    "0.02",
    "0.018",
    "0.015",
    "0.0125",
    "0.01",
]

code_vec: list[str] = []
noise_vec: list[str] = []
for p in p_vec:
    code_vec.append("hgp")
    noise_vec.append(f"depolarize(p={p})")


@arguably.command
def main(*, target_precision: float = 0.04, slurm_maximum_jobs: int = 100):
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
        slurm_maximum_jobs=slurm_maximum_jobs,
    )


if __name__ == "__main__":
    arguably.run()
