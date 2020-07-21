# Benchmarks

This repository contains instructions for benchmarking evm implementations, ewasm contracts and standalone wasm modules. Directory descriptions follow.

```
evm/            - contains benchmarks for different evm implementations (geth and parity)
ewasm/          - contains benchmarks and tests for ewasm contracts in ewasm engines.
wasm/           - contains benchmarks for wasm modules in standalone wasm engines.
wasm-engines/   - contains benchmarks for wasm modules comparing wasm engines and rust native.
```

## EVM

Directory `/evm` contains a list of the current benchmarked evm implementations:

```
evm/
  geth/
  parity/
```

Build each one of the evm implementations:

```bash
(cd evm/geth && docker build . -t geth-bench)
(cd evm/parity && docker build . -t parity-bench)
```

Run EVM benchmarks:

```bash
(cd evm/ && ./scripts/run_bench.sh)
```

The previous command will create a new directory `evmraceresults` and `benchmark_results_data`, containing the following files:

- _evm_benchmarks.csv_ - consolidated benchmarks
- _evm_benchmarks_parity.csv_ - parity benchmarks
- _evm_benchmarks_geth.csv_ - geth benchmarks

Run precompiles benchmarks:

- Geth:
```bash
(cd evm/ && ./scripts/run_precompiles_bench.py geth)
```

- Parity
```bash
(cd evm/ && ./scripts/run_precompiles_bench.py parity)
```

### Wasm Engines And Native Benchmarks

Build the docker image:

```bash
(cd wasm-engines && docker build . -t wasm-engines)
```

Run the docker container:

```bash
docker run --privileged -v $(pwd)/wasm-engines/wasmfiles:/wasmfiles -v $(pwd)/benchmark_results_data:/benchmark_results_data --security-opt seccomp=$(pwd)/wasm-engines/dockerseccompprofile.json -it wasm-engines /bin/bash
```

Build the wasm binaries and execute benchmarks:

```bash
root@docker# ./bench_wasm_and_native.sh
```

## Generate charts using jupyter notebooks

Install python deps for plotting benchmark graphs:

```bash
$ pip install -r requirements.txt
```

Launch a server to access generated charts in Jupyter notebooks:

```bash
$ cd notebooks
$ jupyter-notebook
```

Follow the instructions on the console to access the notebook from the browser.

## Generate charts using python script

Execute the python script:

```bash
$ cd scripts
$ python3 generate_report.py
```
