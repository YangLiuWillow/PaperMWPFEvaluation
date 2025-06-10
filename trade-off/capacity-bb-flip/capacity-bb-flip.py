import os
import arguably

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"


noise: str = "flip(p=0.01)"
code: str = "bb(n=90,k=8,d=10)"

decoder_vec = []

# add mwpf decoders
c_vec = list(range(10)) + list(range(10, 50 + 1, 5)) + [100, 150, 200, 300, 500, 1000]
for c in c_vec:
    decoder_vec.append(f"mwpf(c={c})")

decoder_vec.append("none")

# add BP decoders
bp_step: int = 50
max_iter_vec = (
    list(range(bp_step, 100, bp_step))
    + list(range(100, 1000 + 1, bp_step * 10))
    + list(range(1000, 10000 + 1, bp_step * 100))
)
for max_iter in max_iter_vec:
    decoder_vec.append(f"bposd(max_iter={max_iter},ms_scaling_factor=0.9)")


@arguably.command
def main(*, target_precision: float = 0.04):
    from qec_lego_bench.notebooks.compare_decoder import (
        notebook_compare_decoder,
    )

    assert (
        is_m4pro_cpu()
    ), "evaluation should run on Apple M4 pro CPU. if you're sure running this on another machine, please comment out this assertion."

    num_p_cores: int = 8  # M4 Pro has 8 performance cores

    notebook_compare_decoder(
        notebook_filepath=notebook_filepath,
        code=code,
        noise=noise,
        decoder=decoder_vec,
        target_precision=target_precision,
        local_maximum_jobs=num_p_cores - 2,
    )


def is_m4pro_cpu() -> bool:
    import cpuinfo  # pip install py-cpuinfo

    return cpuinfo.get_cpu_info().get("brand_raw") == "Apple M4 Pro"


if __name__ == "__main__":
    arguably.run()
