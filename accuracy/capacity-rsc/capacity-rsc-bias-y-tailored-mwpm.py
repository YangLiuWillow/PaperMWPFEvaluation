"""
Add evaluation data from the tailored MWPM decoder using implementation in QEC-Playground:
https://github.com/yuewuo/QEC-Playground

cargo run --release -- tool benchmark '[5]' '[0]' '[0.13]' --decoder tailored-mwpm --decoder-config '{"pcmg":true}' --bias-eta 1e200 --code-type rotated-tailored-code --enable-visualizer --visualizer-filename xzzx-bias-y-d5.json --visualizer-model-graph --visualizer-model-hypergraph

cargo run --release -- tool benchmark '[5]' '[0]' '[0.13]' --decoder tailored-mwpm --decoder-config '{"pcmg":true}' --bias-eta 1e200 --code-type rotated-tailored-code


To install and run this script, you need to download the current QEC-Playground code
https://github.com/yuewuo/QEC-Playground/tree/8ec15409e5981c0f18ea43b75bd5d9456dfb41b2
and then run
```sh
cargo install --path .

# then we can use
qecp-cli tool benchmark '[5]' '[0]' '[0.13]' --decoder tailored-mwpm --decoder-config '{"pcmg":true}' --bias-eta 1e200 --code-type rotated-tailored-code
```

"""

import os
import time
import shutil
import json
import re
from tqdm import tqdm
import importlib

this_dir = os.path.dirname(__file__)

spec = importlib.util.spec_from_file_location(
    "capacity_rsc_bias_y", os.path.join(this_dir, "capacity-rsc-bias-y.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

code_vec: list[str] = module.code_vec
noise_vec: list[str] = module.noise_vec
decoder_vec: list[str] = ["tailored-mwpm"] + module.decoder_vec
notebook_filepath: str = module.notebook_filepath[:-6] + "-tailored-mwpm.ipynb"

original_data = os.path.join(this_dir, "capacity-rsc-bias-y.json")
new_data = os.path.join(this_dir, "capacity-rsc-bias-y-tailored-mwpm.json")

if not os.path.exists(new_data):
    shutil.copyfile(original_data, new_data)


with open(original_data, "r") as f:
    data = json.load(f)

with open(new_data, "r") as f:
    data.update(json.load(f))


def main():
    for id, job in tqdm(data.items()):
        if job["result"]["results"].get("tailored-mwpm"):
            continue

        code = job["kwargs"]["code"]
        noise = job["kwargs"]["noise"]
        d = int(re.search(r"css_rsc\(d=(\d+)\)", code).group(1))
        p = float(re.search(r"biased\(p=(\d+\.\d+),basis=Y,eta=inf\)", noise).group(1))

        shots = int(job["shots"])

        # Run QEC-Playground benchmark command
        cmd = f"qecp-cli tool benchmark '[{d}]' '[0]' '[{p}]' --decoder tailored-mwpm --decoder-config '{{\"pcmg\":true}}' --bias-eta 1e200 --code-type rotated-tailored-code --max-repeats {shots} --min-failed-cases {shots} --parallel 0"

        # print(f"Running command: {cmd}")
        start_time = time.time()
        result = os.popen(cmd).read()
        end_time = time.time()
        elapsed = end_time - start_time

        # Parse the output to get error count
        lines = result.strip("\r\n ").split("\n")
        data_line = lines[-1]
        spt = data_line.split(" ")
        assert len(spt) >= 9
        assert int(spt[1]) == d
        error_count = int(spt[4])
        actual_shots = int(spt[3])
        assert actual_shots >= shots
        scaled_error_count = int(error_count * shots / actual_shots)

        job["result"]["results"]["tailored-mwpm"] = {
            "errors": scaled_error_count,
            "discards": 0,
            "elapsed": elapsed,
        }

        # Save updated data
        with open(new_data, "w") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
