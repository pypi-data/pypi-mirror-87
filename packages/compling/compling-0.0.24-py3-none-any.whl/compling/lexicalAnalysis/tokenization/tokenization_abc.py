import abc
import compling.nlp
from typing import *


class Tokenization(metaclass=abc.ABCMeta):
    """
    Tokenization converts input text to streams of tokens, where each token is a separate word, punctuation sign,
    number/amount, date, etc.
    """

    def __init__(self) -> None:
        """
        **\_\_init\_\_**: Creates a new Tokenization object.
        """

        # natural language processing object
        self.nlp = compling.nlp.NLP()

        self.text_key = self.nlp.config.get(s='Corpus', k='text_key')
        self.date_format = self.nlp.config.get(s='Corpus', k='date_format')

    @abc.abstractmethod
    def ngrams2tokens(self,
                      n: Union[int, Iterable[int]],
                      docs_in: Iterable[Dict[str, str]],
                      docs_out: Iterable[Dict[str, str]],
                      pos: Tuple[str, ...] = ("PROPN", "VERB", "NOUN", "ADJ"),
                      corpus_threshold: int = 50,
                      doc_threshold: int = 0,
                      len_gram: int = 3,
                      include: Tuple[str, ...] = None,
                      replace: bool = True) -> Iterable[Dict[int, str]]:
        """
        Calculates frequent n-grams in the corpus. They will be considered as unique tokens during the Tokenization task. <br/>
        Frequent n-grams will be calculated based on the documents in the input stream (docs_in). <br/>
        Frequent n-grams will be considered as unique tokens in the output stream documents (docs_out).

        Args:
           docs_in (Iterable[Dict[str, str]]): Stream of input json documents as dicts. <br/> Each document must have a key where the text of the document is stored. Frequent n-grams will be calculated by scrolling this stream.
           docs_out (Iterable[Dict[str, str]]): Stream of output json documents as dicts. <br/> Each document must have a key where the text of the document is stored. Frequent n-grams will be considered as unique tokens for each document in the stream. Each document will be yielded as output of this function.
           n (Union[int, Iterable[int]]): If int, the size of n-grams. (e.g. n=2, bigrams) <br/> If Iterable[int], the sizes of n-grams. (e.g. n=[2,3,5], bigrams, trigrams, fivegrams)
           pos (Tuple[str, ...], optional): default ('PROPN', 'VERB', 'NOUN', 'ADJ'). <br/> Part of speech of the first and the last token that make up n-grams. <br/> Filters the most informative n-grams. <br/> If None, the filter will be ignored.

                   Example:
                   pos = ("PROPN", "VERB", "NOUN", "ADJ")

                   These n-grams are IGNORED:
                   - "of a": of [ADP], a [DET]
                   - "at home":  at [ADP], home [NOUN]
                   - "as much then": as [ADP], as [ADP]
                   - "a computer scientist": a [DET], scientist [NOUN]
                   - "of natural phenomena": of [ADP], phenomena [NOUN]
                   - ...

                   These n-grams are CONSIDERED:
                   * "mother Earth": mother [NOUN], Earth [PROPN]
                   * "John likes": John [PROPN], likes [VERB]
                   * "computer scientist": computer [NOUN], scientist [NOUN]
                   * "Galilean scientific method": Galilean [ADJ], method [NOUN]
                   * "understanding of natural phenomena": understanding [NOUN], phenomena [NOUN]
                   ...

           corpus_threshold (int, optional, default=50): Filters n-grams that have a corpus frequency greater than corpus_threshold.
           doc_threshold (int, optional, default=0): Filters n-grams that have frequency greater than doc_threshold. <br/> The frequency of an n-gram in the corpus is the sum of the frequency of that n-gram in documents where the ngram occurs at least doc_thresold times.
           len_gram (int, optional, default=3): The size of the first and the last token that make up n-grams must be at least 'len_gram'.

                   Example:
                   len_gram = 5

                   These n-grams are IGNORED:
                   - "John likes": John [4], likes [5]
                   - "New York":  New [3], York [3]
                   - ...

                   These n-grams are CONSIDERED:
                   * "mother Earth": mother [6], Earth [5]
                   * "computer scientist": computer [8], scientist [9]
                   ...

           include (Tuple[str, ...], optional, default=None): Include a list of arbitrary n-grams.
           replace (bool, optional, default=True): If True, replaces a n-gram with its tokens separated by '_'. <br/> Else, concatenates a new token, made merging the n-gram tokens with '_', to the n-gram.

                   Example:

                    - replace = True:
                      "New York is the most populous city in the United States."
                       ->
                      "New_York is the most populous city in the United_States."

                    - replace = False:
                      "New York is the most populous city in the United States."
                       ->
                      "New York New_York is the most populous city in the United States United_States."

        Returns:
            Iterable[Dict[str, str]]: Stream of json documents (docs_out) with frequent n-grams considered as unique token.


            It will be setted _self.corpus_ngram_ (Dict[str, int]): N-grams as keys, frequencies as values. <br/> The frequencies of the n-grams included arbitrarily are set to 0.

                    Example:
                    include = ("Giorgio Napolitano")

                     {
                        "New York": 51,
                        "Giorgio Napolitano": 0,
                        ...
                        "Donald Trump": 402
                     }
        """

    @abc.abstractmethod
    def run(self,
            docs: Iterable[Dict[str, str]],
            doc_id: int = 0,
            token_id: int = 0,
            sent_id: int = 0,
            para_id: int = 0,
            para_size: int = 3,
            index_doc: bool = True,
            index_sent: bool = True,
            index_para: bool = True) -> Iterable[Dict[str, dict]]:
        """
        Runs the tokenization for each document of the corpus.

        Args:
            docs (Iterable[Dict[str, str]]): Stream of json documents as dicts. <br/> Each document must have a key where the text of the document is stored. Each document will be tokenized.
            doc_id (int, optional, default=0): Unique document identifier. <br/> Numeric id of documents. <br/> A progressive id will be assigned to the documents starting from this number.
            token_id (int, optional, default=0): Unique token identifier. <br/> Numeric id of tokens. <br/> A progressive id will be assigned to the tokens starting from this number.
            sent_id (int, optional, default=0): Unique sentence identifier. <br/> Numeric id of sentences. <br/> A progressive id will be assigned to the sentences starting from this number.
            para_id (int, optional, default=0): Unique paragraph identifier. <br/> Numeric id of paragraphs. <br/> A progressive id will be assigned to the paragraphs starting from this number.
            para_size (int, optional, default=3): The paragraph size: the number of sentences that makes up a paragraph.
            index_doc (bool, optional, default=True): If True, returns the records of the documents index as values of the key 'documents'.
            index_sent (bool, optional, default=True): If True, returns the records of the sentences index as values of the key 'sentences'.
            index_para (bool, optional, default=True): If True, returns the records of the paragraphs index as values of the key 'paragraphs'.

        Returns:
            Iterable[Dict[str, dict]]: Stream of tokens, sentences, paragraphs, documents records.

                    Example:
                    [index_sent == True, index_para == False, index_doc == True]

                    >>> t = Tokenizer(domain_stopwords=my_domain_stopwords)
                    >>> records = t.run(docs=my_docs):
                    >>> next(records).keys()
                    dict_keys(["tokens", "sentences", "documents"])


                    Example:
                    >>> record = next(records)
                    >>> tokens = record["tokens"]
                    >>> sentences = record["sentences"]
                    >>> print(tokens)
                    [
                        {
                        "token_id_": 0,
                        "sent_id_": 0,
                        "para_id_": 0,
                        "doc_id_": 0,
                        "text_": "When",
                        "sent_pos_": 0,
                        "para_pos_": 0,
                        "doc_pos_": 0,
                        "lower_": "when",
                        ...
                        },
                        ...
                    ]
                    >>> print(sentences)
                    [
                        {
                         "sent_id_": 0,
                         "text_": "When We , though all unworthy , were called to succeed on the Apostolic Throne the meek Pius X , whose life of holiness and well doing was cut short by grief -atti_degli_apostoli- the fratricidal struggle that had just burst forth in Europe , We , too , on turning a fearful glance on the blood stained battlefields , felt the anguish of a father , who sees his homestead devastated and in ruins before the fury of the hurricane .",
                         "named_entities_": ["Apostolic Throne", "Pius X", "Europe"],
                        ...
                        }
                    ]


                Check the config.ini file for records information.
        """
