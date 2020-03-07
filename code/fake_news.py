import pandas as pd
import numpy as np
# from boilerpipe.extract import Extractor


def main():

    dataset = process_data()

def process_data():

    pd.options.mode.chained_assignment = None # disable warning

    # Read in ad-fonts dataset
    path = '../data/ad-fontes-media.csv'
    df = pd.read_csv(path, delimiter = ',', header=0)
    df = df.rename(columns={'Quality': 'Truth'})

    # Extract relevant columns
    ad_fontes_data = df[['Url', 'Truth']]

    # Turn truth value into a binary class
    ad_fontes_data['Truth'] = np.where(ad_fontes_data['Truth'] > 24, 1, 0)


    # Read in politifact datasets
    fake_data = pd.read_csv('../data/politifact_fake.csv', delimiter = ',', header=0)
    real_data = pd.read_csv('../data/politifact_real.csv', delimiter = ',', header=0)

    # Add truth column
    fake_data['Truth'] = 0
    real_data['Truth'] = 1

    # Combine datasets
    politifact_data = pd.concat([fake_data, real_data])

    # Extract relevent columns
    politifact_data = politifact_data.rename(columns={'news_url':'Url'})
    politifact_data = politifact_data[['Url', 'Truth']]


    # Combine datasets
    all_data = pd.concat([ad_fontes_data, politifact_data])

    return all_data



if __name__ == '__main__':
    main()