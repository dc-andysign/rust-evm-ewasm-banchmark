#!/usr/bin/python3

import csv
import os
import time
import datetime
import shutil

INDIVIDUAL_EVM_RESULTS_CSV_PATH = "/evmraceresults/"
RESULT_CSV_OUTPUT_PATH = "/benchmark_results_data/"
EVMS = ["parity", "geth"]
RESULT_CSV_FILENAME = "evm_benchmarks.csv"
RESULT_FILE = os.path.join(RESULT_CSV_OUTPUT_PATH, RESULT_CSV_FILENAME)

# merge benchmarks from multiple engines into one csv output
def main():
    merged_csv_contents = 'engine, test_name, total_time, gas_used\n'
    evm_results = []

    for evm in EVMS:
        path = os.path.join(INDIVIDUAL_EVM_RESULTS_CSV_PATH, "evm_benchmarks_{}.csv".format(evm))
        data_file = open(path, 'r')
        data = data_file.read().splitlines()
        data_file.close()
        evm_results.append(data)

    for i in range(1, len(evm_results[0])):
        for e in range(0, len(EVMS)):
            merged_csv_contents += evm_results[e][i] + '\n'


    # move existing csv file to backup-datetime-folder
    ts = time.time()
    date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    ts_folder_name = "backup-{}-{}".format(date_str, round(ts))
    dest_backup_path = os.path.join(RESULT_CSV_OUTPUT_PATH, ts_folder_name)

    # back up existing result csv file
    if os.path.isfile(RESULT_FILE):
        os.makedirs(dest_backup_path)
        shutil.move(RESULT_FILE, dest_backup_path)
        print("existing {} moved to {}".format(RESULT_CSV_FILENAME, dest_backup_path))

    with open(RESULT_FILE, 'w') as bench_result_file:
        bench_result_file.write(merged_csv_contents)

    print("saved evm results to:", RESULT_FILE)


if __name__ == "__main__":
    main()
