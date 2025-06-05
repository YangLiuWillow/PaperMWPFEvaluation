import os
import arguably
import multiprocessing

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

decoder_vec = ["chromobius", "mwpf(c=0)", "mwpf(c=200)"]
p_d_vec = [
    ("0.4", [3, 5, 7, 9, 11]),
    ("0.3", [3, 5, 7, 9, 11]),
    ("0.2", [3, 5, 7, 9, 11]),
    ("0.15", [3, 5, 7, 9, 11]),
    ("0.14", [3, 5, 7, 9, 11]),
    ("0.13", [3, 5, 7, 9, 11]),
    ("0.12", [3, 5, 7, 9, 11]),
    ("0.1", [3, 5, 7, 9, 11]),
    ("0.05", [3, 5, 7, 9, 11]),
    ("0.02", [3, 5, 7, 9, 11]),
    ("0.015", [11]),  # add this data point to check the behavior
    ("0.01", [11]),  # add this data point to check the behavior
    ("0.03", [11]),
    ("0.04", [11]),
    # the mwpf(c=50) seems to go across the chromobius line at p=0.01 and I need
    # p=0.015 to confirm this behavior; this suggests that larger p requires
    # larger c to reach a high accuracy, and as physical error rate decreases,
    # it requires even smaller c to reach the same accuracy
    ("0.01", [3, 5, 7]),
    ("0.005", [3, 5]),
    ("0.002", [3]),
    ("0.001", [3]),
]


code_vec: list[str] = []
noise_vec: list[str] = []
for p, d_vec in p_d_vec:
    for d in d_vec:
        code_vec.append(f"css_color(d={d},color=1)")
        noise_vec.append(f"depolarize(p={p})")


@arguably.command
def main(*, target_precision: float = 0.04, slurm_maximum_jobs: int = 50):
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
        max_shots=1000_000_000,
        slurm_maximum_jobs=slurm_maximum_jobs,
    )


if __name__ == "__main__":
    arguably.run()
