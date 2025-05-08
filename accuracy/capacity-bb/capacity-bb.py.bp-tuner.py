"""
We need to compare BP-OSD decoder with MWPF decoder family.

Here we run the parameter tuning for BP-OSD decoder.

# when using slurm, use the following command:
> srun --time=1-00:00:00 --mem=20G --cpus-per-task=4
"""

import os
import arguably
import multiprocessing
from slugify import slugify

local_maximum_jobs: int = multiprocessing.cpu_count()

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

code = "bb(n=90,k=8,d=10)"
noise = "depolarize(p=0.025)"  # use a larger physical error rate because otherwise the simulation is too slow
decoders = [
    "bposd",
    "bposd(osd_order=10,osd_method=cs)",
    "mwpf(bp=1,c=50)",
    "mwpf(bp=1,c=0)",
]


@arguably.command
def main(*, target_precision: float = 0.04):

    with multiprocessing.Pool(len(decoders)) as pool:
        pool.map(task, zip(decoders, [target_precision] * len(decoders)))


def task(data: tuple[str, float]):
    decoder, target_precision = data
    from qec_lego_bench.notebooks.bp_tuner import notebook_bp_tuner

    print(f"{decoder} running on process: {os.getpid()}")

    notebook_bp_tuner(
        notebook_filepath=notebook_filepath[:-6] + f".{slugify(str(decoder))}.ipynb",
        code=code,
        noise=noise,
        decoder=decoder,
        target_precision=target_precision,
    )


if __name__ == "__main__":
    arguably.run()
