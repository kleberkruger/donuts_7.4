#!/usr/bin/env python3

import argparse, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def collect_data_1(csv_data):
    data = []
    last = 0
    for line in csv_data:
        now = int(line)
        time = abs(now - last)
        last = max(last, now)
        data.append(time)
    return data


def collect_data_2(csv_data):
    times = []
    for line in csv_data:
        # times.append(int(line))
        times.append(float(line) / 1000000.0)  # / 1000000 (ns to ms)
    data = []
    last = 0
    for now in sorted(times):
        data.append(now - last)
        last = now
    return data


def remove_outliers(data, outlier = 0.5):
    x = pd.Series(data)  # 200 values
    x = x[x.between(x.quantile(0.0), x.quantile(1.0 - (outlier / 100.0)))]  # without outliers
    return x
    # an_array = np.array(data)
    # mean = np.mean(an_array)
    # standard_deviation = np.std(an_array)
    # distance_from_mean = abs(an_array - mean)
    # max_deviations = 2
    # not_outlier = distance_from_mean < max_deviations * standard_deviation
    # no_outliers = an_array[not_outlier]
    # return no_outliers


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('-b', '--bins', type=int, default=32)
    args = parser.parse_args()
    filepath = os.path.splitext(args.filepath)[0]

    print(("[HISTOGRAM] [ Generating histogram from file: '{}.csv' ]".format(filepath)))
    
    with open(filepath + '.csv') as csv_file:
        data = sorted(collect_data_2(csv_file)) # sorted apenas para entregar os bins ordenados
    
    data = remove_outliers(data, 0.4)
    # print(data)
    # for d in data:
    #     print(d)

    letter = {
        'leslie3d': 'a',
        'bwaves': 'b',
        'lbm': 'c'
    }

    plt.style.use('seaborn-whitegrid')
    plt.figure(figsize=(10, 5))
    # plt.xlim(0, 1.8)
    # plt.ylim(0, 0.6)
    plt.hist(data, weights=np.ones(len(data)) / len(data))
    # plt.title('({}) - Histograma de {}'.format(letter[filepath], filepath))
    plt.title('Histogram of {}'.format(filepath))
    plt.xlabel('Time (ms) without write in NVM')
    plt.ylabel('Percentage of write accesses')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    
    if os.path.isfile(filepath + '.png'):
        os.remove(filepath + '.png')
    plt.savefig(filepath + '.png')
    # plt.savefig(filepath + '.svg')
    plt.savefig(filepath + '.pdf')

    print(("[HISTOGRAM] [ Histogram generated at: '{}.pdf' ]".format(filepath)))


if __name__ == "__main__":
    main()