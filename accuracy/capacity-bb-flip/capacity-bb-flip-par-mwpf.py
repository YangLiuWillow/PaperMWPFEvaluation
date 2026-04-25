import os
import arguably
import multiprocessing

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

code_dict: dict[int, str] = {
    72: "bb(n=72,k=12,d=6)",
    90: "bb(n=90,k=8,d=10)",
    108: "bb(n=108,k=8,d=10)",
    144: "bb(n=144,k=12,d=12)",
    288: "bb(n=288,k=12,d=18)",
}

decoder_vec = ["mwpf(c=0)", "par_mwpf(c=0,thread_pool_size=16)", "par_mwpf(c=50,thread_pool_size=16)", "par_mwpf(c=50,p=4,thread_pool_size=16)"]
p_d_vec = [
    ("0.4", [72]),
]

code_vec: list[str] = []
noise_vec: list[str] = []
for p, n_vec in p_d_vec:
    for n in n_vec:
        code_vec.append(code_dict[n])
        noise_vec.append(f"flip(p={p})")


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
        slurm_cores_per_node=4,
    )


if __name__ == "__main__":
    arguably.run()
