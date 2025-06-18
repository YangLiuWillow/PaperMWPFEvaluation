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


"""
When running the evaluation, I used the following command to minimize impact of multiple cores
```sh
python3 capacity-rsc-d7.py
sudo renice -n -20 -p 47074 

# for debugging or testing plotting, use 1% samples
python3 capacity-rsc-d7.py --shots 10000000
```
"""


@arguably.command
def main(
    *,
    unit_shots: int = 10_000_000,
    shots: int = 1_000_000_000,
    local_maximum_jobs: int = 1,
):
    from qec_lego_bench.notebooks.trace_distribution import (
        notebook_trace_distribution,
    )

    assert (
        is_m4pro_cpu()
    ), "evaluation should run on Apple M4 pro CPU. if you're sure running this on another machine, please comment out this assertion."

    num_p_cores: int = 8  # M4 Pro has 8 performance cores

    notebook_trace_distribution(
        notebook_filepath=notebook_filepath,
        code=code,
        noise=noise,
        decoder=decoders,
        unit_shots=unit_shots,
        shots=shots,
        local_maximum_jobs=(
            num_p_cores - 2 if local_maximum_jobs is None else local_maximum_jobs
        ),
    )


def is_m4pro_cpu() -> bool:
    import cpuinfo  # pip install py-cpuinfo

    return cpuinfo.get_cpu_info().get("brand_raw") == "Apple M4 Pro"


if __name__ == "__main__":
    arguably.run()
