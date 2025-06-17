import os
import arguably

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

code = "css_rsc(d=7)"
noise = "depolarize(p=0.01)"
decoders = [
    "mwpf(c=0)",  # p_L = 5.7e-6
    "mwpf(c=15)",  # p_L = 4.4e-6 (middle point)
    "mwpf(c=200)",  # p_L = 3.2e-6
    # "fb",
    # "fb(max_tree_size=0)",
]


@arguably.command
def main(
    *,
    unit_shots: int = 10_000_000,
    shots: int = 10_000_000,
):
    from qec_lego_bench.notebooks.trace_distribution import (
        notebook_trace_distribution,
    )

    # assert (
    #     is_m4pro_cpu()
    # ), "evaluation should run on Apple M4 pro CPU. if you're sure running this on another machine, please comment out this assertion."

    num_p_cores: int = 8  # M4 Pro has 8 performance cores

    notebook_trace_distribution(
        notebook_filepath=notebook_filepath,
        code=code,
        noise=noise,
        decoder=decoders,
        unit_shots=unit_shots,
        shots=shots,
        local_maximum_jobs=num_p_cores - 2,
    )


def is_m4pro_cpu() -> bool:
    import cpuinfo  # pip install py-cpuinfo

    return cpuinfo.get_cpu_info().get("brand_raw") == "Apple M4 Pro"


if __name__ == "__main__":
    arguably.run()
