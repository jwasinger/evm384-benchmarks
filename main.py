import shlex
import subprocess
import os
import json

geth_dir = os.path.join(os.getcwd(), "go-ethereum")
evmone_dir = os.path.join(os.getcwd(), "evmone")
evmone_bench_cmd = "{}/build/bin/evmone-bench".format(evmone_dir) + " --benchmark_format=json --benchmark_color=false {} 00 \"\""
geth_evm_cmd = "{}/build/bin/evm".format(geth_dir) +  " --statdump --codefile {} --bench run"

pushpop_file = "pushpop_bench.hex"
evm384push_file = "evm384push_bench.hex"

evm384_op_bench_files = {
    #'addmod384': 'evm384_addmod5000.hex',
    'mulmodmont384_5000': 'evm384_mulmodmont50000.hex',
    'mulmodmont384_50000': 'evm384_mulmodmont50000.hex',
    #'submod384': 'evm384_submod5000.hex',
    'keccak_5000': 'keccak5000_bench.hex',
    'keccak_50000': 'keccak50000_bench.hex',
}

from datetime import datetime

import nanoduration

def parse_geth_evm_gas(output):
    for line in output.split("\n"):
        if line.startswith('EVM gas used:    '):
            return int(line.strip('EVM gas used:    '))

    raise Exception("gas not found in output")

# parse geth execution time into seconds
def parse_geth_evm_exec_time(output):
    for line in output.split("\n"):
        if line.startswith('execution time:  '):
            duration = nanoduration.from_str(line.strip('execution time:  '))
            return duration.total_seconds()

    raise Exception("execution time not found in output")

def parse_geth_output(geth_output):
    gas = parse_geth_evm_gas(geth_output)
    time = parse_geth_evm_exec_time(geth_output)
    return gas, time

# geth evm bench tool outputs everything in stderr.. so that's fun
def invoke_geth_evm(engine_cmd):
    proc = subprocess.Popen(engine_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, output = proc.communicate()
    result = output.decode('utf-8')
    print("geth output from {} is {}".format(engine_cmd, result))
    return result

def parse_evmone_output(evmone_output):
    output_json = json.loads("".join(evmone_output.split('\n')[1:]))
    time = str(output_json['benchmarks'][0]['real_time']) + output_json['benchmarks'][0]['time_unit']
    time = nanoduration.from_str(time)
    gas = int(output_json['benchmarks'][0]['gas_used'])
    return gas, time

def invoke_evmone(engine_cmd):
    proc = subprocess.Popen(shlex.split(engine_cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderr = proc.communicate()

    # TODO throw if err
    
    result = output.decode('utf-8')
    print("evmone output from {} is {}".format(engine_cmd, result))
    return result

def bench_engine(engine, evm384_op_name, evm384_bench_code_file):
    engine_cmd = ""
    if engine == "geth":
        engine_cmd = geth_evm_cmd
    elif engine == "evmone":
        engine_cmd = evmone_bench_cmd

    evm384push_bench_cmd = engine_cmd.format(evm384_bench_code_file)
    evm384push_lines = None
    evm384push_bench_gas, evm384push_bench_time = None, None

    if engine == "geth":
        evm384push_lines = invoke_geth_evm(evm384push_bench_cmd)
        evm384push_bench_gas, evm384push_bench_time = parse_geth_output(evm384push_lines)
    elif engine == "evmone":
        evm384push_lines = invoke_evmone(evm384push_bench_cmd)
        evm384push_bench_gas, evm384push_bench_time = parse_evmone_output(evm384push_lines)

    # get evm384push_bench_time, evm384push_gas

    # evm384_estimated_gas = estimate_evm384_gas(evm384push_bench_gas, evm384push_bench_time, pushpop_bench_gas, pushpop_bench_time, 5000)
    # print("estimated gas cost for {} in {} is {}".format(evm384_op_name, engine, evm384_estimated_gas))

def estimate_evm384_gas(evm384push_bench_gas, evm384push_bench_time, pushpop_bench_gas, pushpop_bench_time, num_bench_iterations):
# n = 5000
    # pushpop_time = pushpop_bench_time / num_bench_iterations
    # evm384push_time = evm384_bench_time / num_bench_iterations

    push16_gas = 3
    pop_gas = 1

    # evm384_push_time == evm384_gas + push16_gas
    # pushpop_time == push16_gas + pop_gas

    # gas_rate = pushpop_time / push_bench_gas = evm384_push_time / evm384_bench_time
    #   = pushpop_time / (push16_gas + pop_gas) == evm384_push_time / (evm384_gas + push16_gas)
    #   (evm384_gas + push16_gas) / (push16_gas + pop_gas) = evm384_push_time / pushpop_time
    #   (evm384_gas + push16_gas) = (evm384_push_time * (push16_gas + pop_gas) ) / pushpop_time
    #   ---
    #   evm384_gas = ((evm384_push_time * (push16_gas + pop_gas) ) / pushpop_time ) - push16_gas

    evm384push_bench_time /= num_bench_iterations
    pushpop_bench_time /= num_bench_iterations

    #import pdb; pdb.set_trace()
    return int(((evm384push_bench_time * (push16_gas + pop_gas) ) / pushpop_bench_time ) - push16_gas)


# engine_time_avg = push_gas + pop_gas
# t1 / n * (push_gas + pop_gas) = t2 / n * (evm384_gas  + push_gas)

# n = 5000

if __name__ == "__main__":
    for opname, bench_file in evm384_op_bench_files.items():
        bench_engine("geth", opname, bench_file)
        bench_engine("evmone", opname, bench_file)
