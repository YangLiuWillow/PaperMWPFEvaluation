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

decoder_vec = ["mwpf(c=0)", "mwpf(c=50)"]
p_n_vec = [
    ("0.003", [72, 90, 144]),  # 4e-2, .., 8e-2
    ("0.0025", [72, 90, 144]),  # 2e-2, .., 2e-2
    ("0.002", [72, 90, 144]),  # 7e-3, .., 5e-3
    ("0.0015", [72, 90, 144]),  # 2e-3, .., 2e-3
    ("0.0012", [72, 90, 144]),  # 8e-4, .., 3e-4
    ("0.001", [72, 90, 144]),  # 3.9e-4, .., 9e-5
    ("0.0008", [72, 90, 144]),
    ("0.0006", [72, 90]),
    ("0.0005", [72]),
]

code_vec: list[str] = []
noise_vec: list[str] = []
for p, n_vec in p_n_vec:
    for n in n_vec:
        code_vec.append(f"{code_dict[n][:-1]},p={p})")
        noise_vec.append(f"none")


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
        high_pL_threshold=0.1,
    )


if __name__ == "__main__":
    arguably.run()
