import pandas as pd
import numpy as np


def main():

    dataset = pd.read_csv('../data/processed-dataset.csv',
                          delimiter=',', header=0)

    print(dataset.loc[dataset['Truth'] == 0])
    print(dataset.loc[dataset['Truth'] == 1])


if __name__ == '__main__':
    main()
