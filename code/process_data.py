import pandas as pd
import numpy as np
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import words, stopwords
import re


def main():

    # Process and combine datasets
    combined_dataset = retrieve_data()

    # Extract article text from URLs
    extracted_text_dataset = extract_text(combined_dataset)

    # Extract vocabulary and word counts from article text
    processed_text_dataset = process_text(extracted_text_dataset)

    # Store processed dataset in a CSV
    processed_text_dataset.to_csv(
        '../data/processed-dataset.csv', index=False, header=True)

    print(processed_text_dataset)


def retrieve_data():

    pd.options.mode.chained_assignment = None  # disable warning

    print('PROCESSING AD-FONTS-MEDIA DATA...')

    # Read in ad-fonts dataset
    path = '../data/ad-fontes-media.csv'
    df = pd.read_csv(path, delimiter=',', header=0)
    df = df.rename(columns={'Quality': 'Truth'})

    # Extract relevant columns
    ad_fontes_data = df[['Url', 'Truth']]

    # Turn truth value into a binary class
    ad_fontes_data['Truth'] = np.where(ad_fontes_data['Truth'] > 24, 1, 0)

    print('PROCESSING POLITIFACT DATA...')

    # Read in politifact datasets
    fake_data = pd.read_csv(
        '../data/politifact_fake.csv', delimiter=',', header=0)
    real_data = pd.read_csv(
        '../data/politifact_real.csv', delimiter=',', header=0)

    # Add truth column
    fake_data['Truth'] = 0
    real_data['Truth'] = 1

    # Combine politifact datasets
    politifact_data = pd.concat([fake_data, real_data]).reset_index(drop=True)

    # Extract relevent columns
    politifact_data = politifact_data.rename(columns={'news_url': 'Url'})
    politifact_data = politifact_data[['Url', 'Truth']]

    print('PROCESSING GOSSIPCOP DATA...')

    # Read in gossipcop datasets
    gossipcop_data = pd.read_csv(
        '../data/gossipcop_fake.csv', delimiter=',', header=0)

    # Add truth column
    gossipcop_data['Truth'] = 0

    # Extract relevent columns
    gossipcop_data = gossipcop_data.rename(columns={'news_url': 'Url'})
    gossipcop_data = gossipcop_data[['Url', 'Truth']]

    # Combine datasets
    politifact_and_gossipcop = pd.concat([politifact_data, gossipcop_data]
                                         ).reset_index(drop=True)
    all_data = pd.concat([ad_fontes_data, politifact_and_gossipcop]
                         ).reset_index(drop=True)

    return all_data


def extract_text(original_dataset):

    print('EXTRACTING ARTICLE TEXT FROM URLS...')

    new_dataset = pd.DataFrame(columns=['Url', 'ArticleText', 'Truth'])

    for row in range(len(original_dataset.index)):

        example = {}

        try:
            # Extract article text from url
            url = original_dataset.at[row, 'Url']
            article = Article(url=url, MIN_WORD_COUNT=300,
                              fetch_images=False, http_success_only=True, language='en')
            article.download()
            article.parse()
            print('Retrieved:', article.title)

            # Add new row to dataset
            example['Url'] = url
            example['ArticleText'] = article.text
            example['Truth'] = original_dataset.at[row, 'Truth']
            new_dataset = new_dataset.append(example, ignore_index=True)

        except Exception as e:
            # Skip to next row if the article was not able to be retrieved
            print('Exception at row ', row, ': ', e)
            continue

    return new_dataset


def process_text(dataset):

    print("PROCESSING ARTICLE TEXT...")

    # Get list of stopwords
    nltk.download('stopwords')
    stops = set(stopwords.words('english'))

    # Get list of english words
    nltk.download('words')
    english_words = np.unique(words.words())

    # Extract vocabulary from article text
    vectorizer = CountVectorizer(
        stop_words=stops, tokenizer=tokenizer, vocabulary=english_words)
    X = vectorizer.fit_transform(dataset['ArticleText'])

    # Create new dataframe with vocabulary and labels
    vect_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names())
    new_dataset = pd.concat([vect_df, dataset['Truth']], axis=1)

    # Remove empty columns
    new_dataset = new_dataset.loc[:, (new_dataset != 0).any(axis=0)]

    return new_dataset


def tokenizer(text):
    porter_stemmer = PorterStemmer()
    tokens = re.sub(r"[^A-Za-z0-9\-]", " ", text).lower().split()
    # stemmed_words = [porter_stemmer.stem(word) for word in tokens]
    return tokens


if __name__ == '__main__':
    main()
