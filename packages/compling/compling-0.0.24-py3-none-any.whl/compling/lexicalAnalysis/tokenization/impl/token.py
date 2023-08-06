from compling.nlp import NLP
from compling.config import ConfigManager
from spacy.tokens.token import Token as SpacyToken
from typing import Dict
import compling.lexicalAnalysis.tokenization.token_abc as abctoken
from compling.descriptor import f2att


class Token(abctoken.Token):
    """
    Represents a generic **token**, which is a sequence of characters in the input.
    A token is identified using a tokenizer, which breaks up the sequence of characters in the input into a sequence
    of tokens.
    """

    def __init__(self,
                 token_id: int,
                 token: SpacyToken,
                 nlp: NLP,
                 config: ConfigManager,
                 sent_id: int,
                 para_id: int,
                 doc_id: int,
                 sent_pos: int,
                 para_pos: int,
                 doc_pos: int,
                 is_negated: bool,
                 metadata: dict) -> None:
        """
        Represents a generic **token**, which is a sequence of characters in the input.
        A token is identified using a tokenizer, which breaks up the sequence of characters in the input into a sequence
        of tokens.



        Args:
           token_id (int): Unique token identifier.
           token (SpacyToken): A SpacyToken object.
           nlp (NLP): A Natural Language Processing object.
           config (ConfigManager): A Config manager object.
           sent_id (int): Unique sentence identifier. The id of the sentence the token occurs in.
           para_id (int): Unique paragraph identifier. The id of the paragraph the token occurs in.
           doc_id (int): Unique document identifier. The id of the document the token occurs in.
           sent_pos (int): Position index of the token in the sentence.
           para_pos (int): Position index of the token in the paragraph.
           doc_pos (int): Position index of the token in the document.
           metadata (dict): Token metadata as a key-value pairs.

        Returns:
           None.
        """

        # unique identifiers
        self.token_id_ = token_id
        self.sent_id_ = sent_id
        self.para_id_ = para_id
        self.doc_id_ = doc_id

        # Spacy Token
        self.token = token

        # Natural Language Object
        self.nlp = nlp

        # Text
        self.text_ = self.text()

        # position index
        self.sent_pos_ = sent_pos
        self.para_pos_ = para_pos
        self.doc_pos_ = doc_pos

        # inversion polarity
        self.is_negated_ = is_negated

        # add some field only if the value in config.ini file is True
        for k, v in config.get_section(s='Token_record').items():
            if int(v):
                setattr(self, k + '_', getattr(self, k)())

        # add metadata for this token record
        self.add_metadata(metadata)

    @f2att
    def text(self) -> str:
        """Returns the text of the token."""

        # Avoid exceptions in mongodb
        text = self.token.text.replace('.', '/u002E')

        if not self.nlp.is_ngram(text) or text.endswith("__"):
            return text
        else:
            # elif self.nlp.is_ngram(text) and not text.endswith("__"):
            # e.g. ngram: __middle_east__
            # a token may be: __middle_east__ern
            # so --> __middle_eastern__
            return "__" + text.replace("__", "") + "__"

    @f2att
    def sentiment(self) -> Dict[str, float]:
        """
        Returns the token polarities. <br/>
        Each polarity value is between 0 and 1. <br/>
        _p_ in _[0,1]_

        Returns:
            Dict[str, float]: Polarities type as keys, sentiment values as values.

                    Example:
                    token.text="fuck"

                    >> token.sentiment()
                    {
                     'pos' : 0.0,
                     'neg' : 1.0,
                     'obj' : 0.0
                    }
        """

        if self.pos() not in ('ADJ', 'ADV', 'AUX', 'NOUN', 'PROPN', 'VERB'):
            return {'pos': 0.0, 'neg': 0.0, 'obj': 0.0}

        prefix = "NOT_"
        text = self.lemma()

        if self.is_negated():
            text = prefix + text

        return self.nlp.token_sentiment(text)

    def shape(self) -> str:
        """
        Returns a transformed token version to show orthographic features of the token.

        Alphabetic characters are replaced by x or X, and numeric characters are replaced by d, and sequences of the
        same character are truncated after length 4. For example, "Xxxx" or "dd".
        """
        return self.token.shape_

    def lower(self) -> str:
        """Returns the lowercase version of the token text."""
        return self.nlp.lower(self.text())

    @f2att
    def stem(self) -> str:
        """Returns the stem of the token text."""

        return self.nlp.stem(self.text())

    def lemma(self) -> str:
        """Returns the lemma of the token text."""
        return self.token.lemma_.lower()

    def pos(self) -> str:
        """Returns the pos tag of the token text."""
        return self.token.pos_

    def dep(self) -> str:
        """Returns the dep tag of the token text."""
        return self.token.dep_

    def lang(self) -> str:
        """Returns the language of the token."""
        return self.nlp.nlp_language.iso639

    @f2att
    def is_stopword(self) -> bool:
        """Returns True if the token text is a stopword else False."""

        return self.nlp.is_stopword(self.text())

    @f2att
    def is_ngram(self) -> bool:
        """Returns True if the token text is a ngram else False."""

        return self.nlp.is_ngram(self.text())

    def is_digit(self) -> bool:
        """Returns True if the token text is a digit else False."""
        return self.nlp.is_digit(self.text())

    def is_upper(self) -> bool:
        """Returns True if the token text is upper else False."""
        return self.text().isupper()

    def is_capitalize(self) -> bool:
        """Returns True if the token text is capitalize else False."""
        return self.nlp.is_capitalize(self.text())

    def is_punct(self) -> bool:
        """Returns True if the token text is a punctuation symbol else False."""
        return self.nlp.is_punct(self.text())

    def is_space(self) -> bool:
        """Returns True if the token text is a space character else False."""
        return self.nlp.is_space(self.text())

    def is_bracket(self) -> bool:
        """Returns True if the token text is a bracket symbol else False."""
        return self.token.is_bracket

    def is_ascii(self) -> bool:
        """Returns True if the token text is encoded in ascii else False."""
        return self.token.is_ascii

    def is_negated(self) -> bool:
        """Returns True if the token text is negated in the sentence."""
        return self.is_negated_

    def add_metadata(self, metadata: dict) -> None:
        """Adds metadata as attributes of the token."""

        for k, v in metadata.items():
            if hasattr(self, k + '_'):
                continue
            setattr(self, k + '_', v)

    def to_dict(self) -> dict:
        """Converts the token object to a dict record."""

        return {k: v for k, v in self.__dict__.items() if k.endswith('_')}
