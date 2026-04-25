import os
import arguably
import multiprocessing

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

local_cpu_count: int = multiprocessing.cpu_count()

noise_vec: list[str] = ["depolarize(p=0.001)"]
# start with large d to minimize cold start scheduling problem for very small d
d_vec = list(reversed([9]))
# d_vec = list(reversed([3, 5, 7, 9, 13, 15, 19, 23, 27, 35, 43, 53, 65, 81, 99]))
code_vec: list[str] = [f"css_rsc(d={d})" for d in d_vec]

decoder_vec = []

# add mwpf decoders for comparison
# c_vec = [0, 50, 200]
c_vec = [0]
for c in c_vec:
    decoder_vec.append(f"mwpf(c={c})")

# add UF and MWPM decoder with fusion blossom
# decoder_vec.append("fb(max_tree_size=0)")
# decoder_vec.append("fb")

# add par-mwpf decoders with fixed p=2, varying thread_pool_size
for t in [1, 2, 4, 8, 16, 32]:
    decoder_vec.append(f"par_mwpf(c=0,p=4,thread_pool_size={t})")

# decoder_vec.append("par_mwpf(c=50)")
# decoder_vec.append("par_mwpf(c=50,p=4)")
# decoder_vec.append("par_mwpf(c=200)")


@arguably.command
def main(
    *,
    min_shots: int = 1_000_000,
    max_shots: int = 1000_000_000,
    min_time: float = 0,
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
    )


if __name__ == "__main__":
    arguably.run()
