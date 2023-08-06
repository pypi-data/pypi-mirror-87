from tqdm import tqdm
import copy
import math
from typing import *
from collections import defaultdict
from compling.lexicalAnalysis.vectorization.nevectorization import NEVectorization

class NEVectorizer(NEVectorization):
    """
    The process of converting text into vector is called vectorization.
    The set of corpus documents vectorized corpus makes up the Vector Space Model, which can have a sparse or
    dense representation.

    A NEVectorization object allows you to create vectors grouping named_entities for arbitrary fields.

    Grouping named_entities by:

       * _doc_id_: you 're creating document vectors;
       * _sent_id_: you 're creating sentence vectors;
       * _author_: you're creating author vectors (each named_entities must have an 'author' field);
       ...

    You can group by multiple fields.

    It offers several functions to set the vector components values, such as:

       * **One-hot encoding** (binary values 0/1);
       * **Tf** (Term Frequency);
       * **TfIdf** (Term Frequency Inverse Document Frequency);
       * **MI** (Mutual Information)

    You can specify the vectorization representation format: Term x Document matrix, Postings list.
    """

    def postings2docterm(self, postings: Dict[str, dict]) -> Iterable[dict]:
        """
        Converts a postings list to docterm matrix.

        Args:
            postings (Dict[str, dict]): Postings list.

                    Example:
                    >> print(postings)
                    {
                     "ne1":
                           {
                             "doc1": frequency1,
                             ...
                           },
                     ...
                     }

        Returns:
            Iterable[dict]: Docterm matrix.

                    Example:
                    >> print(next(postings2docterm(postings)))
                    {
                     "doc": "doc1",
                     "bow":
                           {
                            ne1: frequency1,
                            ...
                            }
                     }
        """

        docterm = defaultdict(dict)
        for named_entity in postings:
            for doc, relevance in postings[named_entity].items():
                docterm[doc].update({named_entity: relevance})

        for doc in docterm:
            yield {self.group_by_field_key: doc, 'bow': docterm[doc]}

    def docterm2postings(self, docterm: Iterable[dict]) -> Dict[str, dict]:
        """
        Converts a docterm matrix to a postings list.

        Args:
            docterm (Iterator[dict]): Docterm matrix.

                    Example:
                    >> print(next(docterm))
                    {
                     "doc": "doc1",
                     "bow":
                           {
                            ne1: frequency1,
                            ...
                            }
                     }
                     # bow: Bag of Words
        Returns:
            Dict[str, dict]: Postings list.

                    Example:
                    >> print(docterm2postings(docterm))
                    {
                     "ne1":
                           {
                             "doc1": frequency1,
                             ...
                           },
                     ...
                     }
        """

        postings = defaultdict(dict)
        for record in docterm:
            for named_entity, relevance in record['bow'].items():
                postings[named_entity].update({record[self.group_by_field_key]: relevance})

        return postings

    def tf(self, index: Iterable[dict],
           min_len: int = 0,
           min_count: int = 0,
           format_: str = "docterm-matrix",
           boolean=False) -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates Term Frequency.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).

                    Example:
                    >>> sentence = next(sentences)
                    >>> print(sentence)
                    {
                    "sent_id_": 0,
                    "text_": "When We , though all unworthy , were called to succeed on the Apostolic Throne the meek Pius X [...]",
                    "lemma_": "when -PRON- , though all unworthy , be call to succeed on the Apostolic Throne the meek Pius X [ ... ]",
                    [...]
                    "named_entities_": [{"text_": "Apostolic Throne", "start":12, "sent_pos_end_":13}, {"text_": "Pius X", "start": 16, "sent_pos_end_":17}],
                    ...
                    }

            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

            boolean (bool, optional, default=False): If True return Boolean Vectors else Term Frequency. <br/> If True, the result is the same as onehot method.

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.

                    Example:
                    [format_ == "postings-list"]

                    {
                        "named_entity1":
                              {
                                "doc1": tf1,
                                ...
                              },
                        ...
                    }

                     Example:
                    [format_ == "docterm-matrix"]

                    [{
                        "doc": "doc1",
                        "bow":
                              {
                               named_entity1: tf1,
                               ...
                               }
                    },
                    ...
                    ]
        """

        if not hasattr(self, 'tf_postings'):

            def __filter__(__ne__):
                if len(__ne__) < min_len:
                    return False
                return True

            postings = defaultdict(lambda: defaultdict(int))
            for doc in tqdm(index, desc="TF calculation in progress...", position=0, leave=True):

                key = " + ".join([doc[g] for g in self.group_by_field]).replace('.', '\u002E')

                for ne in doc[self.ne_field]:
                    if len(ne['text_']) < min_len:
                        continue
                    else:
                        named_entity = ne["text_"]

                        if boolean:
                            postings[named_entity][key] = 1
                        else:
                            postings[named_entity][key] += 1

            for named_entity in copy.deepcopy(postings):
                if sum(postings[named_entity].values()) < min_count:
                    del postings[named_entity]

            self.tf_postings = postings

        if format_ == 'postings-list':
            return self.tf_postings
        else:
            return self.postings2docterm(self.tf_postings)

    def reset_tf(self):
        """If present, removes the tf postings list from memory.
         It will be re-calculated on the next run call."""
        if hasattr(self, 'tf_postings'):
            delattr(self, 'tf_postings')

    def tfidf(self,
              index: Iterable[dict],
              normalize=True,
              min_len=0,
              min_count: int = 0,
              format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates Term Frequency Inverse Document Frequency.


        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).

                    Example:
                    >>> sentence = next(sentences)
                    >>> print(sentence)
                    {
                    "sent_id_": 0,
                    "text_": "When We , though all unworthy , were called to succeed on the Apostolic Throne the meek Pius X [...]",
                    "lemma_": "when -PRON- , though all unworthy , be call to succeed on the Apostolic Throne the meek Pius X [ ... ]",
                    [...]
                    "named_entities_": [{"text_": "Apostolic Throne", "start":12, "sent_pos_end_":13}, {"text_": "Pius X", "start": 16, "sent_pos_end_":17}],
                    ...
                    }

            normalize (bool, optional, default=True): If True, normalizes TF for max(TF).
            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.

                    Example:
                    [format_ == "postings-list"]

                    {
                        "named_entity1":
                              {
                                "doc1": tfidf1,
                                ...
                              },
                        ...
                    }

                     Example:
                    [format_ == "docterm-matrix"]

                    [{
                        "doc": "doc1",
                        "bow":
                              {
                               named_entity1: tfidf1,
                               ...
                               }
                    },
                    ...
                    ]
        """

        postings = self.tf(index=index, min_len=min_len, min_count=min_count, format_='postings-list')

        docterm = self.postings2docterm(postings)
        max_tf = {}
        n = 0
        for doc in docterm:
            n += 1
            max_tf[doc[self.group_by_field_key]] = max(doc['bow'].values())

        # Corpus size: the number of documents in the corpus
        N = n

        # The tf_dict will be update to tfidf_dict
        tfidf_postings = copy.deepcopy(postings)

        bar = tqdm(total=len(tfidf_postings), desc="TFIDF calculation in progress... ", position=0, leave=True)

        # For each named_entity in the postings list
        for named_entity in tfidf_postings.keys():

            docs = tfidf_postings[named_entity]

            # For each doc which the named_entity occurs in
            for doc, tf in docs.items():
                if normalize:
                    tf = tf / max_tf[doc]

                # Document Frequency
                df = len(postings[named_entity])

                # Inverse Document Frequency
                idf = math.log(N / df)

                # Term Frequency Inverse Document Frequency
                tfidf_postings[named_entity].update({doc: tf * idf})
            bar.update(1)
        bar.close()

        if format_ == 'postings-list':
            return tfidf_postings
        else:
            return self.postings2docterm(tfidf_postings)

    def mi(self,
           index: Iterable[dict],
           min_len: int = 0,
           min_count: int = 0,
           format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterator[dict]]:
        """
        Calculates Mutual Information.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).

                    Example:
                    >>> sentence = next(sentences)
                    >>> print(sentence)
                    {
                    "sent_id_": 0,
                    "text_": "When We , though all unworthy , were called to succeed on the Apostolic Throne the meek Pius X [...]",
                    "lemma_": "when -PRON- , though all unworthy , be call to succeed on the Apostolic Throne the meek Pius X [ ... ]",
                    [...]
                    "named_entities_": [{"text_": "Apostolic Throne", "start":12, "sent_pos_end_":13}, {"text_": "Pius X", "sent_pos_start_": 16, "sent_pos_end_":17}],
                    ...
                    }

            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.

                    Example:
                    [format_ == "postings-list"]

                    {
                        "named_entity1":
                              {
                                "doc1": mi1,
                                ...
                              },
                        ...
                    }

                     Example:
                    [format_ == "docterm-matrix"]

                    [{
                        "doc": "doc1",
                        "bow":
                              {
                               named_entity1: mi1,
                               ...
                               }
                    },
                    ...
                    ]
        """

        postings = self.tf(index, min_len, min_count, format_='postings-list')
        docterm = {record[self.group_by_field_key]: record for record in self.postings2docterm(postings)}

        # x: group_by_field label
        # y: named_entity
        n_named_entities = sum([sum(postings[named_entity].values()) for named_entity in postings])

        mi_postings = defaultdict(lambda: defaultdict(int))
        for named_entity in tqdm(postings, desc="Mutual Information calculation in progress...", position=0, leave=True):
            posting = defaultdict(int, postings[named_entity])
            for label in posting:
                row = docterm[label]['bow']
                len_x = sum(posting.values())
                len_y = sum(row.values())

                p_x = len_x / n_named_entities
                p_y = len_y / n_named_entities
                p_x_y = posting[label] / n_named_entities

                mi_postings[named_entity][label] = p_x_y * math.log(p_x_y / (p_x * p_y))

        if format_ == 'postings-list':
            return mi_postings
        else:
            return self.postings2docterm(mi_postings)

    def onehot(self, index: Iterable[dict], min_len: int = 0,
               min_count: int = 0, format_: str = 'docterm-matrix') -> Union[Dict[str, dict], Iterable[dict]]:
        """
        Calculates One-hot encoding.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).

                    Example:
                    >>> sentence = next(sentences)
                    >>> print(sentence)
                    {
                    "sent_id_": 0,
                    "text_": "When We , though all unworthy , were called to succeed on the Apostolic Throne the meek Pius X [...]",
                    "lemma_": "when -PRON- , though all unworthy , be call to succeed on the Apostolic Throne the meek Pius X [ ... ]",
                    [...]
                    "named_entities_": [{"text_": "Apostolic Throne", "sent_pos_start_":12, "sent_pos_end_":13}, {"text_": "Pius X", "sent_pos_start_": 16, "sent_pos_end_":17}],
                    ...
                    }

            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            format_ (str, optional, default=docterm-matrix): Format of the vectorization records.

                    Valid input values:
                    ["postings-list", "docterm-matrix"]

        Returns:
            Union[Dict[str, dict], Iterable[dict]]: If format_ == 'postings-list', returns a postings list; else a docterm matrix.

                    Example:
                    [format_ == "postings-list"]

                    {
                        "named_entity1":
                              {
                                "doc1": 0/1,
                                ...
                              },
                        ...
                    }

                     Example:
                    [format_ == "docterm-matrix"]

                    [{
                        "doc": "doc1",
                        "bow":
                              {
                               named_entity1: 0/1,
                               ...
                               }
                    },
                    ...
                    ]
        """
        return self.tf(index, min_len, min_count, boolean=True, format_=format_)

    def run(self, mode: str, index: Iterable[dict], normalize=True,
            min_len=0, min_count=0,
            metadata: Dict[str, dict] = None) -> Iterable[dict]:
        """
        Runs the vectorization grouping named_entities by self.ne_field and self.group_by_field.

        Args:
            mode (str): Vectorization mode. <br/>

                    Valid input values:
                    ["tf", "tfidf", "mi", "onehot"]

            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).

                    Example:
                    >>> sentence = next(sentences)
                    >>> print(sentence)
                    {
                    "sent_id_": 0,
                    "text_": "When We , though all unworthy , were called to succeed on the Apostolic Throne the meek Pius X [...]",
                    "lemma_": "when -PRON- , though all unworthy , be call to succeed on the Apostolic Throne the meek Pius X [ ... ]",
                    [...]
                    "named_entities_": [{"text_": "Apostolic Throne", "sent_pos_start_":12, "sent_pos_end_":13}, {"text_": "Pius X", "sent_pos_start_": 16, "sent_pos_end_":17}],
                    ...
                    }

            normalize (bool, optional, default=True): If True, normalizes TF for max(TF). <br/> This parameter is ignored if mode in ['tf', 'onehot', 'mi'].
            min_len (int, optional, default=0): The minimum length a named_entity must have to be considered. A named_entity must be at least min_len characters long.
            min_count (int, optional, default=0): The minimum frequency a named_entity must have in the corpus to be considered.
            metadata (Dict[str, dict], optional, default=None): A dict containing metadata for each different group_by_field value.  <br/> Each vector will be associated with its own metadata.

                    Example:

                    {
                     "group_by_field1": {
                                         metadata1: 'metadata1',
                                         metadata2: 'metadata2',
                                         ...
                                        },
                     "group_by_field2": {
                                          metadata1: 'metadata11',
                                          metadata2: 'metadata22',
                                         ...
                                        },
                    ...
                    }


        Returns:
            Iterable[dict]: Returns a docterm matrix.

                    Example:
                    >> v = NEVectorizer('doc_id', 'text')
                    >> record = v.run('tfidf', documents)
                    >> print(next(record))
                    {
                        "doc": "doc1",
                        "bow":
                              {
                               ne11: frequency1,
                               ...
                               }
                        metadata1: "metadata1",
                        metadata2: "metadata2",
                        ...
                    }
        """

        # in order to load the vectorization in a mongodb database
        if mode in ['tf', 'onehot']:
            docterm = getattr(self, mode)(index=index, min_len=min_len,
                                          min_count=min_count, format_='docterm-matrix')

        elif mode == 'tfidf':
            docterm = getattr(self, mode)(index=index, normalize=normalize,
                                          min_len=min_len, min_count=min_count,
                                          format_='docterm-matrix')

        # elif mode == 'mi':
        else:
            docterm = getattr(self, mode)(index=index, min_len=min_len,
                                          min_count=min_count,
                                          format_='docterm-matrix')

        # keep the information
        if metadata is not None and len(metadata) > 0:
            for row in docterm:
                record = dict(row)
                record.update(metadata[row[self.group_by_field_key]])
                yield record
        else:
            for row in docterm:
                yield row
