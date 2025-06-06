"""
We will first generate the stim circuits under the `circuits` folder, using the chromobius package

You need to put the chromobius package under the `../chromobius` folder of the git repo.
For example, if the git repo is `~/GitHub/qec-lego-bench`, then you need to put the chromobius package under `~/GitHub/chromobius`.


To debug, use the following command to generate a circuit and then test the logical error rate:
```

~/Documents/GitHub/chromobius/tools/gen_circuits --out_dir ./circuits --stdout --style midout_color_code_X --noise_model uniform --diameter 3 --rounds 3 --noise_strength 0.003 > ./circuits/test.stim && python3 -m qec_lego_bench logical-error-rate 'file(filepath=./circuits/test.stim)' --num-workers=10 --max-shots=1_000_000_000 --decoder 'mwpf(c=200)'
```

"""

import os
import git
import arguably
import multiprocessing

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
circuits_dir = os.path.join(this_dir, "circuits")
git_root_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
chromobius_dir = os.path.join(os.path.dirname(git_root_dir), "chromobius")

assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

decoder_vec = ["mwpf(c=0)", "mwpf(c=200)", "chromobius"]
p_d_vec = [
    # ("0.015", [3, 5, 7]),
    # ("0.01", [3, 5, 7]),
    # ("0.007", [3, 5, 7]),
    # ("0.005", [3, 5, 7]),
    # ("0.003", [3, 5, 7]),
    ("0.002", [3, 5, 7]),
    ("0.001", [3, 5, 7]),
    ("0.005", [3, 5, 7]),
    ("0.003", [3, 5, 7]),
    ("0.002", [3, 5, 7]),
    ("0.001", [3, 5, 7]),
    ("0.0005", [3, 5]),
    ("0.0005", [3, 5]),
    ("0.0003", [3, 5]),
    ("0.0002", [3, 5]),
    ("0.0001", [3]),
    ("0.00005", [3]),
    ("0.00003", [3]),
    ("0.00002", [3]),
    ("0.00001", [3]),
]

if not os.path.exists(circuits_dir):
    os.makedirs(circuits_dir)


def stim_filepath(d: int, p: float):
    return os.path.join(circuits_dir, f"{d}-{p}.stim")


code_vec: list[str] = []
noise_vec: list[str] = []
for p, d_vec in p_d_vec:
    for d in d_vec:
        filepath = stim_filepath(d, p)
        if not os.path.exists(filepath):
            assert os.path.exists(chromobius_dir)
            print(f"stim file {filepath} does not exist, generating...")
            cmd = f"{chromobius_dir}/tools/gen_circuits --out_dir {circuits_dir} --stdout --style midout_color_code_X --noise_model uniform --diameter {d} --rounds {d} --noise_strength {p}"
            result = os.popen(cmd).read()
            assert result.startswith("QUBIT_COORDS")
            with open(filepath, "w") as f:
                f.write(result)
        code_vec.append(f"file(filepath={filepath})")
        noise_vec.append(f"none(p={p})")


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
