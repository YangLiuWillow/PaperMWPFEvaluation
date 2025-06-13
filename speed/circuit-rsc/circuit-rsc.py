import os
import arguably

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"


noise_vec: list[str] = ["none"]
d_vec = list(range(3, 21 + 1, 2))
code_vec: list[str] = [f"rsc(d={d},p=0.001)" for d in d_vec]

decoder_vec = []

# add mwpf decoders
c_vec = [0, 50, 200]
for c in c_vec:
    decoder_vec.append(f"mwpf(c={c})")

# add UF and MWPM decoder with fusion blossom
decoder_vec.append("fb(max_tree_size=0)")
decoder_vec.append("fb")


@arguably.command
def main(
    *,
    min_shots: int = 10000,
    max_shots: int = 1000_000_000,
    min_time: float = 1,
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
