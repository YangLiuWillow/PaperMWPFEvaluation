import os
import arguably
import multiprocessing

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

decoder_vec = ["par_mwpf(c=0)", "par_mwpf(c=50)", "par_mwpf(c=50,p=4)"]

# trimmed for quick testing
p_d_vec = [
    ("0.01", [3, 5]),
    ("0.005", [3, 5]),
    ("0.001", [3]),
]

# full parameter sweep (uncomment for production)
# decoder_vec = ["fb(max_tree_size=0)", "fb", "mwpf(c=0)", "mwpf(c=50)"]
# decoder_vec += ["par_mwpf(c=0)", "par_mwpf(c=50)", "par_mwpf(c=50,p=4)"]
# p_d_vec = [
#     ("0.05", [3, 5, 7]),
#     ("0.02", [3, 5, 7, 9]),
#     ("0.01", [3, 5, 7, 9]),
#     ("0.009", [3, 5, 7, 9, 11]),
#     ("0.008", [3, 5, 7, 9, 11, 13]),
#     ("0.007", [3, 5, 7, 9, 11, 13]),
#     ("0.006", [3, 5, 7, 9, 11, 13]),
#     ("0.005", [3, 5, 7, 9, 11, 13]),
#     ("0.002", [3, 5, 7, 9, 11]),
#     ("0.001", [3, 5, 7]),
#     ("0.0005", [3, 5]),
#     ("0.0002", [3]),
#     ("0.0001", [3]),
# ]

code_vec: list[str] = []
noise_vec: list[str] = []
for p, d_vec in p_d_vec:
    for d in d_vec:
        code_vec.append(f"rsc(d={d},p={p})")
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
