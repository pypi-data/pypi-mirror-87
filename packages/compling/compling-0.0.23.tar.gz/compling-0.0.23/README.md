# compling
#### Computational Linguistic with Python

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

**compling** is a Python module that provides some **_Natural Language Processing_** and **_Computational Linguistics_** functionalities to work with human language data. It incorporates various _Data_ and _Text Mining_ features from other famous libraries (e.g. [spacy](https://pypi.org/project/spacy/), [nltk](https://pypi.org/project/nltk/), [sklearn](https://pypi.org/project/scikit-learn/), ...) in order to arrange a pipeline aimed at the analysis of corpora of _JSON_ documents.

### Documentation
 See documentation [here](http://pycompling.altervista.org/).

### Installation
You can install **compling** with:
```sh
$ pip install compling
```
**compling** requires:
+ _Python_ (>= 3.6)
+ _numpy_
+ _spacy_
+ _nltk_
+ _gensim_
+ _tqdm_
+ _unicodedata2_
+ _unidecode_
+ configparser_
+ _vaderSentiment_
+ _wordcloud_

You also need to download:
* a ++_spacy language model_++ <br/>
See [here](https://spacy.io/models) the available models. You can choose based on the language of your corpus documents. 
By default, **complig** expects you to download _sm_ models. You can still choose to download larger models, but remember to edit the [_confg.ini_](#config.ini) file, so it can work properly.

    _Example_ <br/>
    Let's assume the language of your documents is _English_. 
    You could download the _spacy small english model_:
    ```sh
    python -m spacy download en_core_web_sm
    ```
* some ++_nltk functionalities_++: <br/>
    * _stopwords_
        ```sh
        $ python -m nltk.downloader stopwords
        ```
    * _punkt_
        ```sh
        $ python -m nltk.downloader punkt
        ```
### config.ini
The functionalities offered by **compling** may require a large variety of parameters. To facilitate their use, default values are provided for some parameters:
- some can be changed in the function invocation. Many functions provide optional parameters;
- others are stored in the ++_config.ini_++ file.
  This file configures the processing of your corpora. It contains the values of some special parameters. 
  (e.g. _the language of documents in your corpus._)

You can see a preview below:
```ini
[Corpus]
;The language of documents in your corpus.
language = english

;The standard iso639 of 'language'.
;See: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes .
iso639 = en

;Documents in your corpus store their text in this key.
text_key = text

;Documents in your corpus store their date values as string in this format.
;For a complete list of formatting directives, see: https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior.
date_format = %d/%m/%Y

[Document_record]
;Document records metadata:

;If lower==1, A lowercase version will be stored for each document.
lower = 0

;If lemma==1, A version with tokens replace by their lemma will be stored for each document.
lemma = 0

;If stem==1, A version with tokens replace by their stem will be stored for each document.
stem = 0

;If negations==1, A version where negated token are preceded by 'NOT_' prefix will be stored for each document.
negations = 1

;If named_entities==1, the occurring named entities will be stored in a list for each document.
named_entities = 1
; ...
```
##### ConfigManager
**compling** provides the _ConfigManager_ class to make it easier for you to edit the _config.ini_ file and to help you handling the corpora processing .

You can see the available methods below:
```python
class ConfigManager:
    def __init__(self) -> None:
        """Constructor: creates a ConfigManager object."""

    def load(self) -> None:
        """Loads content of config.ini file."""

    def cat(self) -> None:
        """Shows the content of the config.ini file as plain-text."""

    def updates(self, config:dict) -> None:
        """Updates some values of some sections."""

    def update(self, section, k, v) -> None:
        """Update a k field with a v value in the s section."""

    def reset(self) -> None:
        """Reset the config.ini file to default conditions."""

    def whereisconfig(self) -> str:
        """Shows the config.ini file location."""
```
_**Example of usage**_
```python
from compling.config import ConfigManager
cm = ConfigManager()

# documents of my corpora are italian
cm.updates({'Corpus': {'language': 'italian', 'iso639':'it'})

# I want to keep a lowercase version of each document
cm.update('Document_record', 'lower', '1')

# I changed my mind: reset to default conditions
cm.reset()
```
### Tree structure
The **compling** tree structure is shown below. 
Different fonts are used: 
+ **bold**, for packages; 
+ _italic_, for files; 
+ Capitalized, for available classes.
----------------------
* **compling**
    - ++example-corpus++: folder containing a sample corpus.
        - ++vatican-publications++
            -  _[...]_
    - _config.ini_: configuration file.
    - _config. py_
        - [ConfigManager](#ConfigManager)
    - **nlptoolkit**
        + NLP
    - **analysis** 
        + **lexical**
            +  **tokenization**
                + [Tokenizer](#Tokenization)
            +  **vectorization**
                +  [Vectorizer](#Vectorization)
                +  [VSM](#Vectorization)
            +  **unsupervised_learning**
                +  **clustering**
                    +  [KMeans](#Unsupervised-Learning)
                    +  [Linkage](#Unsupervised-Learning)
                +  **dimensionality reduction**
                    +  [PCA](#Unsupervised-Learning)
                    +  [TruncateSVD](#Unsupervised-Learning)
        + **sentiment**
            + **lexicon**
                + Vader
                + Sentiwordnet
            + [SentimentAnalyzer](####Sentiment-Analysis) 
    - **embeddings**
        + **word**
            + [Word2vec](#Embeddings) 
            + [Fasttext](#Embeddings) 
        + **document**
            + [Doc2vec](#Embeddings) 
            
#### example of usage (compling)
You can see a short example of usage below. See the [documentation](http://pycompling.altervista.org/) for more details.

As example let's use the Vatican Publication corpus provided by **compling**.
```python
import pkg_resources
corpus_path = pkg_resources.resource_filename('compling', 'example-corpus/vatican-publications')

def doc_iterator(path:str):
    """Yields json documents."""
    import os, json

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), mode='r', encoding='utf-8') as f_json:
                    data = json.load(f_json)
                    yield data
```
##### Tokenization
The tokenization converts input text to streams of tokens, where each token is a separate word, punctuation sign, number/amount, date, etc.

**compling** provides a _Tokenizer_ class that tokenizes a stream of json documents.

A Tokenizer object converts the corpus documents into a stream of:

   * _tokens_: tokens occurring in those documents. Each token is characterized by:
      * _token_id_: unique token identifier;
      * _sent_id_: unique sentence identifier. The id of the sentence the token occurs in;
      * _para_id_: unique paragraph identifier. The id of the paragraph the token occurs in;
      * _doc_id_: unique document identifier. The id of the document the token occurs in;
      * _text_: the text of the token;
      * a large variety of _optional meta-information_ (e.g. PoS tag, dep tag, lemma, stem, ...);
   * _sentences_ : sentences occurring in those documents. Each sentence is characterized by:
      * _sent_id_: unique sentence identifier;
      * _para_id_: unique paragraph identifier. The id of the paragraph the sentence occurs in;
      * _doc_id_: unique document identifier. The id of the document the sentence occurs in;
      * _text_: the text of the sentence;
      * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);
   * _paragraphs_: sentences occurring in those documents. Each paragraph is characterized by:
      * _para_id_: unique paragraph identifier;
      * _doc_id_: unique document identifier. The id of the document the paragraph occurs in;
      * _text_: the text of the paragraph;
      * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);
   * _documents_: each document is characterized by:
      * _doc_id_: unique document identifier;
      * _text_: the text of the document;
      * a large variety of _optional meta-information_ (e.g.lemma, stem, ...);

A Tokenizer object is also able to retrieve frequent n-grams (in documents of your corpus) to be considered as unique tokens by tokenization.
```python
from compling.analysis.lexical.tokenization import Tokenizer

# new Tokenizer
t = Tokenizer()

# json doc stream input: from these docs we will calculate frequent corpus n-grams.
docs_in = doc_iterator(corpus_path)

# json doc stream output: we will consider frequent corpus n-grams as unique tokens.
docs_out = doc_iterator(corpus_path)

# let's consider frequent bigrams as unique tokens
docs_out = t.ngrams2tokens(n=2, docs_in=docs_in, docs_out=docs_out)

# run tokenization for each docs
tokenization_records = t.run(docs_out)

token_records = list()
sentence_records = list()
paragraph_records = list()
document_records = list()

# we could store the records: if your corpus is large, tokenization could take a long time.
for doc in tokenization_records:
    token_records.extend(doc['tokens'])
    sentence_records.extend(doc['sentences'])
    paragraph_records.extend(doc['tokens'])
    document_records.extend(doc['paragraphs'])
```
##### Vectorization
The process of converting text into vector is called vectorization. 
The set of corpus documents vectorized corpus makes up the _Vector Space Model_, which can have a sparse or dense representation.

**compling** provides a _Vectorizer_ class that, given corpus tokens records, vectorizes the corpus documents.

A Vectorizer object allows you to create vectors grouping tokens for arbitrary fields.
E.g. grouping tokens by:
- _'doc_id'_: you 're creating document vectors;
- _'sent_id'_: you 're creating sentence vectors;
- _'author'_: you're creating author vectors (each token must have an 'author' field);
- ...
You can also choose the text field the tokens will be grouped by.
- lemma
- text
- stem
- ...

It offers several functions to set the vector components values, such as:
- One-hot encoding
- Tf
- TfIdf
- Mutual Information

You can specify the vectorization representation format: Term x Document matrix, Postings list.

You can also inspect the Vector Space Model. 

**compling** provides a Vector Space Model class. It allows you to analyze the distance between each vectors.

```python
from compling.analysis.lexical.vectorization import Vectorizer

# new Vectorizer
v = Vectorizer(token_field='lemma', group_by_field='author')

# stream of author vectors
vector_stream = v.run('tfidf', tokens_records)
```
```python
from compling.analysis.lexical.vectorization import VSM

# stream to list
vector_list = list(vector_stream)

# new VSM objecy
v = VSM(vectors=vector_list, id_field='author')

# calculates the vector distance matrix between vectors.
v.distance(metric='euclidean')

# plot the distance matrix as a hitmap
v.plot()

# top n values for each vector id
v.topn(n=10)
```
#### Unsupervised Learning
Unsupervised learning is a type of machine learning that looks for previously undetected patterns in a data set with no pre-existing labels and with a minimum of human supervision.

**compling** provides these classes:
- _KMeans_
- _Linkage_
- _PCA_
- _TruncateSVD_
```python
from compling.analysis.lexical.unsupervised_learning.clustering import KMeans

# new Kmeans object
kmeans = KMeans(vectors=vector_list, id_field='author')

# run kmeans: 4 clusters
clusters = kmeans.run(k=4)
```
```python
from compling.analysis.lexical.unsupervised_learning.clustering import Linkage

# new Linkage object
linkage = Linkage(vectors=vector_list, id_field='author')

# run hierarchical clustering
linkage.run(method='complete')

# plot the dendrogram showing the set of all possible clusters
linkage.plot()
```
```python
from compling.analysis.lexical.unsupervised_learning.dimensionality_reduction import PCA

# new PCA object
pca = PCA(vectors=vector_list, id_field='author')

# run PCA: reduction to 2 components.
pca.run(n=2)

# plot 2D vectors
pca.plot()
```
```python
from compling.analysis.lexical.unsupervised_learning.dimensionality_reduction import TruncatedSVD

# new TruncatedSVD object
truncateSVD = TruncatedSVD(vectors=vector_list, id_field='author')

#run TruncatedSVD: reduction to 2 components.
truncateSVD.run(n=2)

# plot 2D vectors
truncateSVD.plot()
```
#### Sentiment Analysis
**compling** implements a _SentimentAnalyzer_ class that allows you to perform sentiment analysis through a lexicon-based approach.

SentimentAnalyzer uses a summation strategy: the polarity level of a document is calculated as the sum of the polarities of all the words in the document.

The analysis detects negation pattern and reverses the negated tokens polarity.

Providing a regex, you can filter sentences/paragraphs/documents to analyze.

Providing a pos list and/or a dep list you can filter the words whose polarities will be summed.

At the moment, only the analysis for English documents is available.
```python
from compling.analysis.sentiment import SentimentAnalyzer
from compling.analysis.sentiment.lexicon import Vader

# new SentimentAnalyzer. 
# polarity of documents as sum of VERB, NOUN, PROPN, ADJ token polarities.
s = SentimentAnalyzer(token_records, text_field='lemma', group_by_field='author',
                      id_index_field='para_id', # you can filter some paragraphs
                      pos=('VERB', 'NOUN', 'PROPN', 'ADJ')) 

# polarity of documents as sum of VERB, NOUN, PROPN, ADJ token polarities occurring in paragraphs filtered by regex_pattern.
s.filter(paragraph_records, regex_pattern="^.*(work).*$")

# new Lexicon    
lexicon = Vader()
  
# run sentiment analysis 
polarities, words = s.run(lexicon=lexicon)
```
#### Embeddings
An embedding is a relatively low-dimensional space into which you can translate high-dimensional vectors. Embeddings make it easier to do machine learning on large inputs like sparse vectors representing words or documents.

**compling** incorporates some gensim class as Word2vec, Fasttext and Doc2vec.
```python
from compling.embeddings.words import Word2vec

# new Word2vec
w = Word2vec(index=sentence_records, text_field='text')

# build Word2vec model
w.run()
        
love_sim = w.most_similar('love')
```
```python
from compling.embeddings.documents import Doc2vec

# new Doc2vec
w = Doc2vec(index=sentence_records, id_field='author', text_field='text')

# build Doc2vec model
w.run()

paulvi_sim = w.most_similar("Paul VI")
```