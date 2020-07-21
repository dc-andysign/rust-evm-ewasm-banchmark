#############
# IMPORTS   #
#############
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
from statistics import mean

#############
# CONSTANTS #
#############
EVM_RESULT_FILE = "evm_benchmarks.csv"
STANDALONE_WASM_RESULT_FILE = "standalone_wasm_results.csv"
NATIVE_RESULT_FILE = "native_benchmarks.csv"

pd.set_option('display.max_rows', 1000)
plt.style.use('ggplot')

# Helpers
def toApropUnit(secs):
	if secs < 0.001:
		μs = secs * 1000000
		return "{}μs".format(round(μs, 1))
	if secs < 1 and secs >= 0.001:
		ms = secs * 1000
		return "{}ms".format(round(ms, 1))


def msToSec(ms):
	return ms / 1000

def sToSec(s):
	return s

# Read CSV Function
def read_results(file_name):
	results = defaultdict(list)
	csv_results = pd.read_csv(file_name)
	return csv_results

def filter_based_on_engine(df, e):
	df_data_filtered=df.copy()
	df_data_filtered=df_data_filtered[df_data_filtered.engine.eq(e)] if e else df_data_filtered
	df_data_filtered=df_data_filtered.reset_index(drop=True)
	df_data_filtered
	return df_data_filtered

def filter_by_averaging_string(df, s):
	l = lambda x: mean( [float(y) for y in x.split(', ')] )
	df_data_filtered = df.copy()
	df_data_filtered[s] = df[s].apply(l)
	return df_data_filtered

def filter_by_converting_time(df, f, s):
	df_data_filtered = df.copy()
	df_data_filtered[""+s] = df_data_filtered[""+s].apply(f)
	return df_data_filtered

def filename_by_virtualisation_type(t):
	return EVM_RESULT_FILE if t=='evm' else (STANDALONE_WASM_RESULT_FILE if t=='wasm' else NATIVE_RESULT_FILE)

def fix_test_name(t, ttype):
	if ttype=='evm':
		if t=='bn128_mul-chfast2':
			return 'bn128_mul_weierstrudel-chfast2'
		if t=='bn128_mul-cdetrio2':
			return 'bn128_mul_weierstrudel-cdetrio2'
		return t
	return t
