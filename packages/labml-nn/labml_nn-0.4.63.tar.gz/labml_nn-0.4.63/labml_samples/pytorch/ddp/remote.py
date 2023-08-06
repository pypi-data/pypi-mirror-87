"""
labml_remote setup
labml_remote rsync
labml_remote update

Test:

source ~/miniconda/etc/profile.d/conda.sh
conda activate labml_sample_env
cd labml_sample/
PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/src" cmd

export GLOO_SOCKET_IFNAME=enp1s0
export NCCL_SOCKET_IFNAME=enp1s0

PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/src" python labml_samples/pytorch/ddp/launch.py --nproc_per_node=2 --nnodes=2 --node_rank=0 --master_addr="104.171.200.232" --master_port=1234 labml_samples/pytorch/ddp/mnist.py
PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/src" python labml_samples/pytorch/ddp/launch.py --nproc_per_node=2 --nnodes=2 --node_rank=1 --master_addr="104.171.200.232" --master_port=1234 labml_samples/pytorch/ddp/mnist.py


RUN_UUID=fba9eb202cb211eba5beacde48001122 PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/src" python -m torch.distributed.launch --nproc_per_node=2 --nnodes=2 --node_rank=0 --master_addr=104.171.200.181 --master_port=1234 labml_samples/pytorch/ddp/mnist.py
RUN_UUID=fba9eb202cb211eba5beacde48001122 PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/src" python -m torch.distributed.launch --nproc_per_node=2 --nnodes=2 --node_rank=1 --master_addr=104.171.200.181 --master_port=1234 labml_samples/pytorch/ddp/mnist.py

RUN_UUID=fba9eb202cb211eba5beacde48001122 PYTHONPATH="${PYTHONPATH}:$(pwd):$(pwd)/src" python -m torch.distributed.launch --nproc_per_node=2 labml_samples/pytorch/ddp/mnist.py
"""

import time

from labml import experiment
from labml_remote.cli import run_command_async

# run_command_async(0, 'python labml_samples/pytorch/ddp/launch.py --nproc_per_node=2 labml_samples/pytorch/ddp/mnist.py'.split(' '))

run_uuid = experiment.generate_uuid()
for i in [0, 1]:
    # python labml_samples/pytorch/ddp/launch.py --nproc_per_node=2 --nnodes=2 --node_rank=0 --master_addr=104.171.200.232 --master_port=1234 labml_samples/pytorch/ddp/mnist.py
    # run_command_async(i, [f'python labml_samples/pytorch/ddp/launch.py --nproc_per_node=2 --nnodes=2 '
    #                       f'--node_rank={i} --master_addr=104.171.200.181 --master_port=1234 '
    #                       f'labml_samples/pytorch/ddp/mnist.py'], {'GLOO_SOCKET_IFNAME': 'enp1s0'})
    run_command_async(i,
                      [f'python -m torch.distributed.launch --nproc_per_node=2 --nnodes=2 '
                       f'--node_rank={i} '
                       f'--master_addr=104.171.200.181 --master_port=1234 '
                       f'labml_samples/pytorch/ddp/mnist.py'],
                      {'GLOO_SOCKET_IFNAME': 'enp1s0',
                       'RUN_UUID': run_uuid})
    time.sleep(5)
