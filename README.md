# EVM384 Gas Benchmarking

A quick experiment which estimates pricing for evm384 opcodes

## Explanation

Two benchmarks:
1) PUSH16 000…000 POP
2) PUSH16 000…000 ADDMOD384

Take a long sequence of these. Let’s say we have these n=100000 times in a sequence (push pop push pop …). Run it with geth or evmone and measure the time (t1 and t2) it takes in each case.

(Note: push\_gas = 3 and pop\_gas = 2)

We know that the gas cost of 1) should be pushpop\_gas = n * (push\_gas + pop\_gas), the runtime of it will be t1, and calculate a t1 / (n * (push\_gas + pop\_gas)), which is 1 gas worth of execution time on that given machine.

Then we take the time (t2) it took to run 2) and calculate total\_gas = t2 / (t1 / (n * (push\_gas + pop\_gas))). We can get the individual evm384 gas: ceil((total\_gas - pushpop\_gas) / n) - push\_gas.

## Usage

### Setup
```
git submodule update --init
(cd go-ethereum && make all)
(cd evmone && git submodule update --init && mkdir build && cd build && cmake -DEVMONE_TESTING=ON .. && make -j4)
```

### Estimate EVM384 v7 opcode pricing for evmone and Geth
```
make benchmark
```
