def gen_montmul_bench_bytecode(n=1):
  # emplace parameters at predefined offsets
  preamble = "7ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776000527fba58c7535798485f455752705358ce776dec56a2971a075c93e480fac35ef6156010527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776038527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156048527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776068527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156078527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce77610190527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156101a052"

  montmul_call = "6f0000012c000000380000006800000000c2" # PUSH16 (offsets for the parameters) + MONTMUL

  code = preamble
  for _ in range(n):
    code += montmul_call

  return code

def gen_addmod384_bench_bytecode(n=1):
  # emplace parameters at predefined offsets
  preamble = "7ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776000527fba58c7535798485f455752705358ce776dec56a2971a075c93e480fac35ef6156010527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776038527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156048527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776068527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156078527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce77610190527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156101a052"

  addmod_call = "6f0000012c000000380000006800000000c0" # PUSH16 (offsets for the parameters) + MONTMUL

  code = preamble
  for _ in range(n):
    code += addmod_call

  return code

def gen_submod384_bench_bytecode(n=1):
  # emplace parameters at predefined offsets
  preamble = "7ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776000527fba58c7535798485f455752705358ce776dec56a2971a075c93e480fac35ef6156010527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776038527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156048527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce776068527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156078527ffdff02000000097602000cc40b00f4ebba58c7535798485f455752705358ce77610190527fba58c7535798485f455752705358ce776dec56a1971a075c93e480fac35ef6156101a052"

  montmul_call = "6f0000012c000000380000006800000000c1" # PUSH16 (offsets for the parameters) + MONTMUL

  code = preamble
  for _ in range(n):
    code += montmul_call

  return code

def gen_keccak_bench_bytecode(size=32,n=1):
  # emplace arbitrary input data for keccak, probably not needed
  preamble = "7f1337000000000000000000000000000000000000000000000000000000000000600052"
  code = preamble

  size_hex = hex(size)[2:]
  assert size < 255, "Size must be < 255"
  if(len(size_hex) == 1):
    size_hex = '0' + size_hex

  for _ in range(n):
    #       PUSH 00 PUSH size_hex  SHA3 POP
    # code += "600060" + size_hex + "2050"
    code += "60" + size_hex + "60002050"

  return code

def save_benchmark(benchmark_file_name, code):
    with open('benchmarks/' + benchmark_file_name, 'w+') as f:
        f.write(code)

if __name__ == "__main__":
  save_benchmark('keccak32_5000_bench.hex', gen_keccak_bench_bytecode(size=32,n=5000))
  save_benchmark('keccak32_50000_bench.hex', gen_keccak_bench_bytecode(size=32,n=50000))

  save_benchmark('keccak136_5000_bench.hex', gen_keccak_bench_bytecode(size=136,n=5000))
  save_benchmark('keccak136_50000_bench.hex', gen_keccak_bench_bytecode(size=136,n=50000))

  save_benchmark('keccak192_5000_bench.hex', gen_keccak_bench_bytecode(size=192,n=5000))
  save_benchmark('keccak192_50000_bench.hex', gen_keccak_bench_bytecode(size=192,n=5000))
  save_benchmark('evm384_addmod_5000_bench.hex', gen_addmod384_bench_bytecode(5000))
  save_benchmark('evm384_addmod_50000_bench.hex', gen_addmod384_bench_bytecode(50000))
  save_benchmark('evm384_submod_5000_bench.hex', gen_submod384_bench_bytecode(5000))
  save_benchmark('evm384_submod_50000_bench.hex', gen_submod384_bench_bytecode(50000))
