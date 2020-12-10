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
    'mulmodmont384_5000': 'evm384_mulmodmont5000.hex',
    'mulmodmont384_50000': 'evm384_mulmodmont50000.hex',
    #'submod384': 'evm384_submod5000.hex',
    'keccak32_5000': 'keccak32_5000_bench.hex',
    'keccak32_50000': 'keccak32_50000_bench.hex',
    'keccak136_5000': 'keccak136_5000_bench.hex',
    'keccak136_50000': 'keccak136_50000_bench.hex',
    'keccak192_5000': 'keccak192_5000_bench.hex',
    'keccak192_50000': 'keccak192_50000_bench.hex',
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
def invoke_geth_evm(bench_code_file):
    engine_cmd = geth_evm_cmd.format(bench_code_file)
    proc = subprocess.Popen(engine_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, output = proc.communicate()
    result = output.decode('utf-8')
    # print("geth output from {} is {}".format(engine_cmd, result))
    return result

def parse_evmone_output(evmone_output):
    output_json = json.loads("".join(evmone_output.split('\n')[1:]))
    time = str(output_json['benchmarks'][0]['real_time']) + output_json['benchmarks'][0]['time_unit']
    time = nanoduration.from_str(time).total_seconds()
    gas = int(output_json['benchmarks'][0]['gas_used'])
    return gas, time

def invoke_evmone(bench_code_file):
    engine_cmd = evmone_bench_cmd.format(bench_code_file)
    proc = subprocess.Popen(shlex.split(engine_cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderr = proc.communicate()

    # TODO throw if err
    
    result = output.decode('utf-8')
    # print("evmone output from {} is {}".format(engine_cmd, result))
    return result

def estimate_evm384_gas(evm384_bench_time, evm_bench_time, evm_bench_gas, num_iterations):
    push_gas = 3

    # evm384_bench_time /= num_iterations
    # evm_bench_time /= num_iterations

    # evm_bench_gas /= num_iterations # doesn't include initial mstore overhead

    return ((evm384_bench_time * evm_bench_gas) / (evm_bench_time * num_iterations)) - push_gas 

# engine_time_avg = push_gas + pop_gas
# t1 / n * (push_gas + pop_gas) = t2 / n * (evm384_gas  + push_gas)

# n = 5000

def bench_op(opname, num_iters, input_size=None, engine_bench_fn=invoke_geth_evm, engine_bench_parse_fn=parse_geth_output):
    if not input_size:
        input_size = ""
    bench_name = "{}{}_{}_bench.hex".format(opname,input_size,num_iters)
    engine_output = engine_bench_fn(bench_name)
    return engine_bench_parse_fn(engine_output)

def bench_mulmontmod384_keccak(engine):
    for bench_iter_count in [5000, 50000]:
        _, evm384_time = bench_op("evm384_mulmodmont", bench_iter_count)

        for keccak_input_size in [32, 136, 192]:
            keccak_gas, keccak_time = bench_op("keccak", bench_iter_count, input_size=keccak_input_size)

            evm384_estimated = estimate_evm384_gas(evm384_time, keccak_time, keccak_gas, bench_iter_count)
            print("geth mulmodmont384 cost estimated against keccak ({} byte input, {} iterations): {}".format(keccak_input_size, bench_iter_count, evm384_estimated))

            keccak_gas, keccak_time = bench_op("keccak", bench_iter_count, input_size=keccak_input_size,engine_bench_fn=invoke_evmone, engine_bench_parse_fn=parse_evmone_output)

            evm384_estimated = estimate_evm384_gas(evm384_time, keccak_time, keccak_gas, bench_iter_count)
            print("evmone mulmodmont384 cost estimated against keccak ({} byte input, {} iterations): {}".format(keccak_input_size, bench_iter_count, evm384_estimated))


if __name__ == "__main__":
    bench_mulmontmod384_keccak("geth")
