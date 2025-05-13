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

decoder_vec = ["bposd(max_iter=1000,ms_scaling_factor=1)"]
p_d_vec = [
    ("0.4", [72, 90, 144]),
    ("0.3", [72, 90, 144]),
    ("0.2", [72, 90, 144]),
    ("0.1", [72, 90, 144]),
    ("0.05", [72, 90, 144]),
    ("0.04", [72, 90, 144]),
    ("0.03", [72, 90, 144]),
    ("0.025", [72, 90, 144]),
    ("0.02", [72, 90, 144]),
    ("0.018", [72, 90]),
    ("0.015", [72, 90]),
    ("0.0125", [72, 90]),
    ("0.01", [72, 90]),
    ("0.0078", [72]),
    ("0.00625", [72]),
    ("0.005", [72, 90]),
    ("0.004", [72]),
    ("0.003", [72]),
    ("0.0025", [72]),
    ("0.002", [72]),
    ("0.0018", [72]),
    ("0.0015", [72]),
    ("0.00125", [72]),
    ("0.001", [72]),
]

# we need to observe more closely how the curve behaves for n=72 between 0.02 and 0.005


code_vec: list[str] = []
noise_vec: list[str] = []
for p, n_vec in p_d_vec:
    for n in n_vec:
        code_vec.append(code_dict[n])
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
    )


if __name__ == "__main__":
    arguably.run()
