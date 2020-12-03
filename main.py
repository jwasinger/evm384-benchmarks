
# args
#   evm384_bench_gas
#   push_bench_gas
#   pushpop_bench_time
#   evm384_bench_time
#   num_bench_iterations

# n = 5000
# pushpop_time = pushpop_bench_time / num_bench_iterations
# evm384push_time = evm384_bench_time / num_bench_iterations

# evm384_push_time == evm384_gas + push16_gas
# pushpop_time == push16_gas + pop_gas

# gas_rate = pushpop_time / push_bench_gas = evm384_push_time / evm384_bench_time
#   = pushpop_time / (push16_gas + pop_gas) == evm384_push_time / (evm384_gas + push16_gas)
# (evm384_gas + push16_gas) / (push16_gas + pop_gas) = evm384_push_time / pushpop_time
# (evm384_gas + push16_gas) = (evm384_push_time * (push16_gas + pop_gas) ) / pushpop_time
# evm384_gas = ((evm384_push_time * (push16_gas + pop_gas) ) / pushpop_time ) - push16_gas

push16_gas = 3
pop_gas = 2

# engine_time_avg = push_gas + pop_gas
# t1 / n * (push_gas + pop_gas) = t2 / n * (evm384_gas  + push_gas)

# n = 5000
