import os
import arguably

this_dir = os.path.dirname(os.path.abspath(__file__))
assert os.path.abspath(__file__)[-3:] == ".py"
notebook_filepath = os.path.abspath(__file__)[:-3] + ".ipynb"


noise: str = "depolarize(p=0.01)"
code: str = "css_rsc(d=7)"

decoder_vec = []

# add UF and MWPM decoder with fusion blossom
t_vec = list(range(10))
for t in t_vec:
    decoder_vec.append(f"fb(max_tree_size={t})")
decoder_vec.append("fb")
decoder_vec.append("none")

# add mwpf decoders
c_vec = list(range(10)) + list(range(10, 50 + 1, 5)) + [100, 150, 200, 300, 500, 1000]
for c in c_vec:
    decoder_vec.append(f"mwpf(c={c})")


@arguably.command
def main(*, target_precision: float = 0.04):
    from qec_lego_bench.notebooks.compare_decoder import (
        notebook_compare_decoder,
    )

    # assert (
    #     is_m4pro_cpu()
    # ), "evaluation should run on Apple M4 pro CPU. if you're sure running this on another machine, please comment out this assertion."

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
