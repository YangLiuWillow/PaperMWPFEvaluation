import os
import arguably
import multiprocessing

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

local_cpu_count: int = multiprocessing.cpu_count()

noise_vec: list[str] = ["none"]
# use large d where parallelism is meaningful
d_vec = list(reversed([21, 31]))
code_vec: list[str] = [f"rsc(d={d},p=0.001)" for d in d_vec]

decoder_vec = []

# serial mwpf baseline
decoder_vec.append("mwpf(c=0)")

# parallel mwpf with fixed p=4, varying thread_pool_size
for t in [1, 2, 4, 8, 16, 32]:
    decoder_vec.append(f"par_mwpf(c=0,p=4,thread_pool_size={t})")


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

    notebook_speed_scaling(
        notebook_filepath=notebook_filepath,
        code=code_vec,
        noise=noise_vec,
        decoder=decoder_vec,
        min_shots=min_shots,
        max_shots=max_shots,
        min_time=min_time,
        local_maximum_jobs=local_cpu_count - 2,
        repeats=5,
        slurm_cores_per_node=32,
        slurm_processes_per_node=1,
        slurm_extra=dict(
            walltime="10:00:00",
            queue="day",
        ),
    )


if __name__ == "__main__":
    arguably.run()
