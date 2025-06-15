import os
import arguably
import git

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"
git_root_dir = git.Repo(".", search_parent_directories=True).working_tree_dir
chromobius_dir = os.path.join(os.path.dirname(git_root_dir), "chromobius")
circuits_dir = os.path.join(this_dir, "circuits")

noise_vec: list[str] = ["none"]
# start with large d to minimize cold start scheduling problem for very small d
d_vec = list(reversed(range(3, 31 + 1, 2)))
# d_vec = [3, 5, 7]
p_str = "0.0001"
code_vec: list[str] = []


if not os.path.exists(circuits_dir):
    os.makedirs(circuits_dir)


def stim_filepath(d: int):
    return os.path.join(circuits_dir, f"{d}.stim")


for d in d_vec:
    filepath = stim_filepath(d)
    if not os.path.exists(filepath):
        assert os.path.exists(chromobius_dir)
        print(f"stim file {filepath} does not exist, generating...")
        cmd = f"{chromobius_dir}/tools/gen_circuits --out_dir {circuits_dir} --stdout --style midout_color_code_X --noise_model uniform --diameter {d} --rounds {d} --noise_strength {p_str}"
        result = os.popen(cmd).read()
        assert result.startswith("QUBIT_COORDS")
        with open(filepath, "w") as f:
            f.write(result)
    code_vec.append(f"file(filepath={filepath})")

decoder_vec = []

decoder_vec.append("chromobius")

# add mwpf decoders
c_vec = [0, 50, 200]
for c in c_vec:
    decoder_vec.append(f"mwpf(c={c})")


@arguably.command
def main(
    *,
    min_shots: int = 10000,
    max_shots: int = 1000_000_000,
    min_time: float = 0,
):
    from qec_lego_bench.notebooks.speed_scaling import (
        notebook_speed_scaling,
    )

    assert (
        is_m4pro_cpu()
    ), "evaluation should run on Apple M4 pro CPU. if you're sure running this on another machine, please comment out this assertion."

    num_p_cores: int = 8  # M4 Pro has 8 performance cores

    notebook_speed_scaling(
        notebook_filepath=notebook_filepath,
        code=code_vec,
        noise=noise_vec,
        decoder=decoder_vec,
        min_shots=min_shots,
        max_shots=max_shots,
        min_time=min_time,
        local_maximum_jobs=num_p_cores - 2,
        repeats=5,
    )


def is_m4pro_cpu() -> bool:
    import cpuinfo  # pip install py-cpuinfo

    return cpuinfo.get_cpu_info().get("brand_raw") == "Apple M4 Pro"


if __name__ == "__main__":
    arguably.run()
