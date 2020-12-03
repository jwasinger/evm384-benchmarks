
# args
#   evm384_bench_gas
#   push_bench_gas
#   pushpop_bench_time
#   evm384_bench_time
#   num_bench_iterations


def invoke_cmd(engine_cmd):
    pass

evmone_bench_cmd = "{}/build/bin/evmone-bench".format(evmone_dir) + " --benchmark_format=json --benchmark_color=false --benchmark_min_time=5 {} 00 \"\""
geth_evm_cmd = "{}/build/bin/evm".format(geth_dir) +  " --statdump --codefile {} --bench"

pushpop_file = "..."
evm384push_file = "..."

def invoke_engine(engine, cmd):
    if engine == "geth":
        pass
    elif engine == "evmone":
        pass

def parse_output(engine, cmd):
    if engine == "geth":
        pass
    elif engine == "evmone":
        pass

def bench_engine(name, cmd):
    # format cmd ...
    # engine_cmd = ...
    pushpop_lines = invoke_engine(engine_cmd.format(pushpop_file))
    evm384push_lines = invoke_engine(engine_cmd.format(evm384push_file))

    bench_result = estimate_evm384_gas(parse_output(name, pushpop_lines, evm384push_lines))

    # print bench_result

def bench_evmone(evm_code_file):
    pass

def estimate_evm384_gas(evm384_bench_gas, push_bench_gas, pushpop_bench_time, evm384_bench_time, num_bench_iterations):
    pass

# n = 5000
    # pushpop_time = pushpop_bench_time / num_bench_iterations
    # evm384push_time = evm384_bench_time / num_bench_iterations

    push16_gas = 3
    pop_gas = 2

    # evm384_push_time == evm384_gas + push16_gas
    # pushpop_time == push16_gas + pop_gas

    # gas_rate = pushpop_time / push_bench_gas = evm384_push_time / evm384_bench_time
    #   = pushpop_time / (push16_gas + pop_gas) == evm384_push_time / (evm384_gas + push16_gas)
    #   (evm384_gas + push16_gas) / (push16_gas + pop_gas) = evm384_push_time / pushpop_time
    #   (evm384_gas + push16_gas) = (evm384_push_time * (push16_gas + pop_gas) ) / pushpop_time
    #   ---
    #   evm384_gas = ((evm384_push_time * (push16_gas + pop_gas) ) / pushpop_time ) - push16_gas


# engine_time_avg = push_gas + pop_gas
# t1 / n * (push_gas + pop_gas) = t2 / n * (evm384_gas  + push_gas)

# n = 5000

if __name__ == "__main__":
    bench_engine("geth", geth_evm_cmd)
    bench_engine("evmone", geth_evm_cmd)
