import os
import arguably

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"


noise_vec: list[str] = ["depolarize(p=0.01)"]
# start with large d to minimize cold start scheduling problem for very small d
"""
def generate_d_vec(ratio: float = 1.244, max_d: int = 99) -> list[int]:
    d = 3
    d_vec = [d]
    while d <= max_d:
        int_d = 2 * round(d / 2) + 1
        if int_d != d_vec[-1]:
            d_vec.append(int_d)
        d *= ratio
    return d_vec
d_vec = generate_d_vec()
"""
# d_vec = list(reversed([3, 5, 7, 9, 13, 15, 19, 23, 27, 35, 43, 53, 65, 81, 99]))
d_vec = list([3, 5, 7, 9, 13, 15, 19, 23, 27, 35, 43, 53, 65, 81, 99])
code_vec: list[str] = [f"css_color(d={d},color=1)" for d in d_vec]

decoder_vec = []

# add mwpf decoders
c_vec = [0, 50, 200]
for c in c_vec:
    decoder_vec.append(f"mwpf(c={c})")

decoder_vec.append("chromobius")


@arguably.command
def main(
    *,
    min_shots: int = 300_000,
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
