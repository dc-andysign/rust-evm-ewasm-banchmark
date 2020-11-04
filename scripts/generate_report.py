import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import durationpy
import math

from os.path import join
from collections import defaultdict
from statistics import mean
import json

from plot_utils import *
# from adjustText import adjust_text

#############
# CONSTANTS #
#############

COLORS_DEFAULT ={'blue': '#348ABD', 'red': '#EC9989'}
CSV_RESULT_DIR = "../benchmark_results_data"
CPU_INFO_FILE = "cpuinfo.txt"
EVM_RESULT_FILE = "evm_benchmarks.csv"
STANDALONE_WASM_RESULT_FILE = "standalone_wasm_results.csv"
NATIVE_RESULT_FILE = "native_benchmarks.csv"

# Show cpuinfo txt
with open(join(CSV_RESULT_DIR, CPU_INFO_FILE), 'r') as cpuinfofile:
	[print(line.rstrip()) for line in cpuinfofile.readlines()]

# Filter
evmdata = read_results(join(CSV_RESULT_DIR, EVM_RESULT_FILE))
gethdata = filter_based_on_engine(evmdata, 'geth-evm')
gethdata = filter_by_converting_time(gethdata, sToSec, ' total_time')
paritydata = filter_based_on_engine(evmdata, 'parity-evm')
paritydata = filter_by_converting_time(paritydata, sToSec, ' total_time')

wasmalldata = read_results(join(CSV_RESULT_DIR, STANDALONE_WASM_RESULT_FILE))
wasmdata = filter_based_on_engine(wasmalldata, 'wasm3')
wasmdata = filter_by_converting_time(wasmdata, sToSec, 'exec_time')

nativealldata = read_results(join(CSV_RESULT_DIR, NATIVE_RESULT_FILE))
nativedata = filter_by_averaging_string(nativealldata, 'elapsed_times')


# All Tests
# FILTER:
# Avaliable tests: 'bn128_mul-chfast2','bn128_mul-cdetrio2'
#         'blake2b-2805-bytes','blake2b-5610-bytes','blake2b-8415-bytes'
#         'sha1-10808-bits','sha1-21896-bits','sha1-42488-bits'
# Engines available for EVM: 'geth-evm', 'parity-evm'
# Engines available for WASM (wasmalldata["engine"].unique()):
#        'wagon', 'wabt', 'v8-liftoff', 'v8-turbofan', 'v8-interpreter',
#        'wasmtime', 'wavm', 'life-polymerase', 'life', 'wasmi',
#        'wamr-interp', 'wamr-jit', 'wamr-aot', 'wasm3'
# Engines available for NATIVE: 'native-rust'
def calc_customtest_by_test_and_filter(test, filters):
	customtest_f, customtest = [], []
	for i in range(len(filters)):
		t = filters[i]['virtualisation_type']
		e = filters[i]['engine']
		c = filters[i]['column']
		p = filters[i]['prefix']
		RESULT_FILE = filename_by_virtualisation_type(t)
		rawdata = read_results(join(CSV_RESULT_DIR, RESULT_FILE))
		rawdata = filter_based_on_engine(rawdata,e)
		edata = filter_by_converting_time(rawdata,sToSec,p+c) if e else rawdata
		edata = filter_by_averaging_string(rawdata,p+c) if not e else edata
		e_customtest_f = mean(edata[edata[p+"test_name"].eq(fix_test_name(test,t))][p+c].tolist())
		e_customtest = toApropUnit(e_customtest_f)
		customtest_f.append(e_customtest_f)
		customtest.append(e_customtest)
	return customtest_f, customtest

def plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,c=[],f='chart.png'):
	plt.close('all')#; plt.figure()
	fig, (ax) = plt.subplots(1, 1, sharey=True, figsize=(13,9))
	vals = customtest_f
	annotates = customtest
	labels = [f['virtualisation_type']+' '+f['engine'] for f in filters]
	y_pos = np.arange(len(vals))
	ax.set_yticklabels(np.arange(len(vals)))
	plt.bar(y_pos, vals, align='center')
	plt.xticks(y_pos, labels)
	plt.title('BenchmarkResults: '+test, color='gray')
	plt.xlabel('Smart Contract Types (Virtualisation)')
	plt.ylabel('Benchmark Results (Elipsed Time)')
	if c == []:
		colors = [ # list('rgbkymc')
			'#EC9989', '#90D1C2', '#90D1C2',
			'#90D1C2', '#D1D191', '#EB65E5',
			'#7DCBF5'
		]
	else:
		colors = c
	for i in range(min(len(vals),len(colors))):
		ax.get_children()[i].set_color(colors[i])
	for i in range(len(ax.patches)):
		p = ax.patches[i]
		note = annotates[i]
		if (vals[i]<0.004):
			h = vals[i]+0.00005
#             0.00005
		else:
			h = vals[i]+0.0002
		ax.annotate(note, (p.get_x()+p.get_width()/2, h+0.00015), ha='center')
	plt.savefig('../charts/'+f)

test = 'bn128_mul-chfast2'
filters = [
	{'virtualisation_type':'evm',   'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'wasm',  'engine':'wasm3',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'native','engine':'',        'prefix':'','column':'elapsed_times'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,['#90D1C2','#EC9989'],'evm-v-wasm-v-native_bn128_mul-chfast2.png')
test = 'bn128_mul-cdetrio2'
filters = [
	{'virtualisation_type':'evm',   'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'wasm',  'engine':'wasm3',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'native','engine':'',        'prefix':'','column':'elapsed_times'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,['#90D1C2','#EC9989'],'evm-v-wasm-v-native_bn128_mul-cdetrio2.png')

test = 'blake2b-2805-bytes'
filters = [
	{'virtualisation_type':'evm',   'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'wasm',  'engine':'wasm3',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'native','engine':'',        'prefix':'','column':'elapsed_times'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,[],'evm-v-wasm-v-native_'+test+'.png')
test = 'blake2b-5610-bytes'
filters = [
	{'virtualisation_type':'evm',   'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'wasm',  'engine':'wasm3',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'native','engine':'',        'prefix':'','column':'elapsed_times'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,[],'evm-v-wasm-v-native_'+test+'.png')
test = 'blake2b-8415-bytes'
filters = [
	{'virtualisation_type':'evm',   'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'wasm',  'engine':'wasm3',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'native','engine':'',        'prefix':'','column':'elapsed_times'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,[],'evm-v-wasm-v-native_'+test+'.png')

test = 'sha1-10808-bits'
filters = [
	{'virtualisation_type':'evm',   'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'wasm',  'engine':'wasm3',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'native','engine':'',        'prefix':'','column':'elapsed_times'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,[],'evm-v-wasm-v-native_'+test+'.png')
test = 'sha1-21896-bits'
filters = [
	{'virtualisation_type':'evm',   'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'wasm',  'engine':'wasm3',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'native','engine':'',        'prefix':'','column':'elapsed_times'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,[],'evm-v-wasm-v-native_'+test+'.png')
test = 'sha1-42488-bits'
filters = [
	{'virtualisation_type':'evm',   'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'wasm',  'engine':'wasm3',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'native','engine':'',        'prefix':'','column':'elapsed_times'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,[],'evm-v-wasm-v-native_'+test+'.png')


# Geth v Parity
def plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,c=list('rgbkymc'),f='chart.png'):
	plt.close('all')#; plt.figure()
	fig, (ax) = plt.subplots(1, 1, sharey=True, figsize=(13,9))
	vals = customtest_f
	annotates = customtest
	labels = [f['virtualisation_type']+' '+f['engine'] for f in filters]
	y_pos = np.arange(len(vals))
	ax.set_yticklabels(np.arange(len(vals)))
	plt.bar(y_pos, vals, align='center')
	plt.xticks(y_pos, labels)
	plt.title('BenchmarkResults: '+test, color='gray')
	plt.xlabel('Smart Contract Types (Virtualisation)')
	plt.ylabel('Benchmark Results (Elipsed Time)')
	colors = c
	for i in range(min(len(vals),len(colors))):
		ax.get_children()[i].set_color(colors[i])
	for i in range(len(ax.patches)):
		p = ax.patches[i]
		note = annotates[i]
		if (vals[i]<0.004):
			h = vals[i]+0.00005
		else:
			h = vals[i]+0.0008
		ax.annotate(note, (p.get_x()+p.get_width()/2, h-0.00001), ha='center')
	plt.savefig('../charts/'+f)

test = 'bn128_mul-cdetrio2'
filters = [
	{'virtualisation_type':'evm', 'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'evm', 'engine':'parity-evm','prefix':' ','column':'total_time'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,['#90D1C2','#EC9989'],'geth-v-parity_'+test+'.png')

test = 'blake2b-2805-bytes'
filters = [
	{'virtualisation_type':'evm', 'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'evm', 'engine':'parity-evm','prefix':' ','column':'total_time'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,['#90D1C2','#EC9989'],'geth-v-parity_'+test+'.png')

test = 'sha1-10808-bits'
filters = [
	{'virtualisation_type':'evm', 'engine':'geth-evm','prefix':' ','column':'total_time'},
	{'virtualisation_type':'evm', 'engine':'parity-evm','prefix':' ','column':'total_time'}]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test,['#90D1C2','#EC9989'],'geth-v-parity_'+test+'.png')


# Engines available for WASM (wasmalldata["engine"].unique()):
def plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test):
	f = 'wasm-all-available-engines.png'
	plt.close('all')#; plt.figure()
	fig, (ax) = plt.subplots(1, 1, sharey=True, figsize=(13,9))
	vals = customtest_f
	annotates = customtest
	labels = [f['engine'] for f in filters]
	y_pos = np.arange(len(vals))
	ax.set_yticklabels(np.arange(len(vals)))
	plt.bar(y_pos, vals, align='center')
	plt.xticks(y_pos, labels, rotation=30)
	plt.title('BenchmarkResults: '+test, color='gray')
	plt.xlabel('Smart Contract Types (Virtualisation)')
	plt.ylabel('Benchmark Results (Elipsed Time)')
	colors = ['#EC9989']*13
	for i in range(min(len(vals),len(colors))):
		ax.get_children()[i].set_color(colors[i])
	for i in range(len(ax.patches)):
		p = ax.patches[i]
		note = annotates[i]
		ax.annotate(note, (p.get_x()+p.get_width()/2, vals[i]+0.00005), ha='center')
	plt.savefig('../charts/'+f)

test = 'bn128_mul-chfast2'
test = 'blake2b-8415-bytes'
test = 'sha1-42488-bits'
filters = [
	{'virtualisation_type':'wasm','engine':'wamr-jit','prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'v8-turbofan',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'wamr-aot','prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'v8-liftoff',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'wasmtime','prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'wasm3','prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'wavm','prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'wamr-interp','prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'life','prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'wabt',    'prefix':'','column':'exec_time'},

	{'virtualisation_type':'wasm','engine':'wagon',   'prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'v8-interpreter','prefix':'','column':'exec_time'},
	{'virtualisation_type':'wasm','engine':'wasmi','prefix':'','column':'exec_time'},
#     {'virtualisation_type':'wasm','engine':'life-polymerase','prefix':'','column':'exec_time'},
]
customtest_f, customtest = calc_customtest_by_test_and_filter(test, filters)
plot_by_customtest_filters_n_test(customtest_f,customtest,filters,test)
