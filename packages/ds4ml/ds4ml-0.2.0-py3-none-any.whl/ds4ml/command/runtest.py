"""
synthesize.py

"""

from ds4ml.dataset import DataSet
from ds4ml.utils import CustomFormatter, read_data_from_csv, file_name, str_to_list

import argparse
import time


def main():

    data = DataSet(read_data_from_csv('/Users/i076744/SAP/Anonymization/adult-pickle.csv'))
    print('------------- data ---------------')
    print('Shape:', data.shape)
    print('age:', data['age'].to_pattern())
    print('age:', data['age'].to_pattern())

    # construct DataSet from pattern file
    dataset = DataSet.from_pattern('adult-pickle_pattern.json')
    print('dataset', dataset)
    print('1: age:', dataset['age'].to_pattern())
    print('1: age:', type(dataset['age']))
    print('2: age:', dataset['age'].to_pattern())
    print('2: age:', type(dataset['age']))

    synthesized = dataset.synthesize(records=6000)
    synthesized.to_csv("adult-pickle-pattern.csv", index=False)

    # duration = time.time() - start
    # print(f'Synthesized data {args.output} in {round(duration, 2)} seconds.')


if __name__ == '__main__':
    main()
