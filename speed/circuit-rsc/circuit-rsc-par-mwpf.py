import os
import arguably
import multiprocessing

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"

local_cpu_count: int = multiprocessing.cpu_count()

noise_vec: list[str] = ["none"]
# start with large d to minimize cold start scheduling problem for very small d
d_vec = list(reversed(range(3, 31 + 1, 2)))
code_vec: list[str] = [f"rsc(d={d},p=0.001)" for d in d_vec]

decoder_vec = []

# add mwpf decoders for comparison
c_vec = [0, 50, 200]
for c in c_vec:
    decoder_vec.append(f"mwpf(c={c})")

# add UF and MWPM decoder with fusion blossom
decoder_vec.append("fb(max_tree_size=0)")
decoder_vec.append("fb")

# add par-mwpf decoders with different partition counts
decoder_vec.append("par_mwpf(c=0)")
decoder_vec.append("par_mwpf(c=50)")
decoder_vec.append("par_mwpf(c=50,p=4)")
decoder_vec.append("par_mwpf(c=200)")


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
    )


if __name__ == "__main__":
    arguably.run()
