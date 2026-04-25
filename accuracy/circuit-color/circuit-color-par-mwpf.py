import os
import arguably
import multiprocessing

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
circuits_dir = os.path.join(this_dir, "circuits")

assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

decoder_vec = ["mwpf(c=0)", "par_mwpf(c=0,thread_pool_size=16)", "par_mwpf(c=50,thread_pool_size=16)", "par_mwpf(c=50,p=4,thread_pool_size=16)"]
p_d_vec = [
    ("0.0003", [3]),
]


def stim_filepath(d: int, p: float):
    return os.path.join(circuits_dir, f"{d}-{p}.stim")


code_vec: list[str] = []
noise_vec: list[str] = []
for p, d_vec in p_d_vec:
    for d in d_vec:
        filepath = stim_filepath(d, p)
        assert os.path.exists(filepath), f"stim file {filepath} does not exist"
        code_vec.append(f"file(filepath={filepath})")
        noise_vec.append(f"none(p={p})")


@arguably.command
def main(*, target_precision: float = 1.0):
    from qec_lego_bench.notebooks.pL_p_compare_decoders import (
        notebook_pL_p_compare_decoders,
    )

    notebook_pL_p_compare_decoders(
        notebook_filepath=notebook_filepath,
        code=code_vec,
        noise=noise_vec,
        decoder=decoder_vec,
        target_precision=target_precision,
        max_shots=10_000_000,
        local_maximum_jobs=local_maximum_jobs - 1,
        high_pL_threshold=0.1,
        slurm_cores_per_node=2,
    )


if __name__ == "__main__":
    arguably.run()
