import pandas as pd
import numpy as np
from newspaper import Article


def main():

    clean_dataset = process_data()
    print(clean_dataset)


def process_data():

    pd.options.mode.chained_assignment = None # disable warning

    print('PROCESSING AD-FONTS-MEDIA DATA...')

    # Read in ad-fonts dataset
    path = '../data/ad-fontes-media.csv'
    df = pd.read_csv(path, delimiter = ',', header=0)
    df = df.rename(columns={'Quality': 'Truth'})

    # Extract relevant columns
    ad_fontes_data = df[['Url', 'Truth']]

    # Turn truth value into a binary class
    ad_fontes_data['Truth'] = np.where(ad_fontes_data['Truth'] > 24, 1, 0)



    print('PROCESSING POLITIFACT DATA...')

    # Read in politifact datasets
    fake_data = pd.read_csv('../data/politifact_fake.csv', delimiter = ',', header=0)
    real_data = pd.read_csv('../data/politifact_real.csv', delimiter = ',', header=0)

    # Add truth column
    fake_data['Truth'] = 0
    real_data['Truth'] = 1

    # Combine politifact datasets
    politifact_data = pd.concat([fake_data, real_data]).reset_index(drop=True)

    # Extract relevent columns
    politifact_data = politifact_data.rename(columns={'news_url':'Url'})
    politifact_data = politifact_data[['Url', 'Truth']]


    # Combine datasets
    all_data = pd.concat([ad_fontes_data, politifact_data]).reset_index(drop=True)

    # Extract article text from URLs
    all_data = extract_text(all_data)

    return all_data



def extract_text(original_dataset):

    print('EXTRACTING ARTICLE TEXT FROM URLS...')

    new_dataset = pd.DataFrame(columns=['Url', 'ArticleText', 'Truth'])

    for row in range(len(original_dataset.index)):

        example = {}

        try:
            # Extract article text from url
            url = original_dataset.at[row, 'Url']
            article = Article(url)
            article.download()
            article.parse()
            print('Retrieved:', article.title)

            # Add new row to dataset
            example['Url'] = url
            example['ArticleText'] = article.text
            example['Truth'] =  original_dataset.at[row, 'Truth']
            new_dataset = new_dataset.append(example, ignore_index=True)

        except Exception as e:
            # Skip to next row if the article was not able to be retrieved
            print('Exception at row ', row, ': ', e)
            continue

    return new_dataset


if __name__ == '__main__':
    main()