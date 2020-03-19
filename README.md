# SENG474 Project

## Data Processing

- To run the data processing script, you need to have newspaper3k and nltk installed. It takes about an hour to run but it outputs a csv file with the processed data, so we won't need to run it each time we train our models.
- The cleaned and processed data can be found in `data/processed-dataset.csv`
- Each row of the csv file contains the number of occurrences of each english word in an article, excluding stop words
- The last column is the label and is 1 is the article is real, 0 if the article is fake.
- I was having problems with stemming the words, but we can take another crack at this if we need to reduce our number of features
- We could also try using sklearn's `TfidfVectorizer` instead `CountVectorizer` later to see if that improves our accuracy

## Attribution

- Article text extraction: [Newspaper3k](https://newspaper.readthedocs.io/en/latest/)
- List of english words and stopwords from the [NLTK Corpus](http://www.nltk.org/data.html)
- Tokenizer and stemming function inspired by [Jonathan Soma's blog](http://jonathansoma.com/lede/algorithms-2017/classes/more-text-analysis/counting-and-stemming/)
