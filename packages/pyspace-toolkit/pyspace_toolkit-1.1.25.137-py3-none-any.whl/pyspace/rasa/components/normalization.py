
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.components import Component
from rasa.nlu.training_data import Message, TrainingData
from rasa.nlu.config import RasaNLUModelConfig

from rasa.nlu.constants import (
    CLS_TOKEN,
    RESPONSE,
    SPARSE_FEATURE_NAMES,
    TEXT,
    TOKENS_NAMES,
    INTENT,
    MESSAGE_ATTRIBUTES,
    ENTITIES,
)

from pyspace.nlp.preprocessing.normalizer.xnormalizer import xNormalizer
# from pyspace.nlp.toolkit.zemberek import normalize, lemmatize

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer

import re
import string

class PyspaceNormalizer(Component):

    def normalize_tokens(self, tokens):
        # [self.normalize_token(t) for t in tokens]
        return False
    def normalize_text(self, text):
        return False

    def normalize_message(self, message):

        if self.normalize_tokens(["message"]) != False:
            
            tokens = [t.text for t in message.data["tokens"] if t.text != '__CLS__']

            ###########################################################################
            
            tokens = self.normalize_tokens(tokens) 

            ###########################################################################

            if self.normalize_text("message") != False:
                norm = self.normalize_text(message.text.replace('__CLS__','').strip())
            else:
                norm = " ".join(tokens)
            message.text = norm
            message.set(TEXT, norm)
            
            tokens = Tokenizer._convert_words_to_tokens(tokens, norm)
            tokens = Tokenizer.add_cls_token(tokens, TEXT)
            message.set(TOKENS_NAMES[TEXT], tokens)
            
        elif self.normalize_text("message") != False:

            norm = self.normalize_text(message.text)

            message.text = norm
            message.set(TEXT, norm)


    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        for message in training_data.training_examples:
            self.normalize_message(message)

    def process(self, message: Message, **kwargs: Any):

        self.normalize_message(message)

##########################################################################################3
##########################################################################################3

class ZemberekNormalizer(PyspaceNormalizer):

    
    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        from pyspace.nlp.toolkit.zemberek import normalize
        self.normalize = normalize
        super().__init__(component_config)
    
    def normalize_text(self, text):
        return self.normalize(text)


class ZemberekLemmatizer(PyspaceNormalizer):

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        from pyspace.nlp.toolkit.zemberek import lemmatize
        self.lemmatize = lemmatize
        super().__init__(component_config)
        
    def normalize_tokens(self, tokens):
        return [self.lemmatize(t) for t in tokens]

class TurkishCharacterNormalizer(PyspaceNormalizer):

    def normalize_tokens(self, tokens):
        return [xNormalizer.tr_normalize(t) for t in tokens]

    def normalize_text(self, text):
        return xNormalizer.tr_normalize(text)

class PunctuationNormalizer(PyspaceNormalizer):

    def normalize_tokens(self, tokens):
        
        output = []
        for t in tokens: 
            temp = re.sub(fr"""[{re.escape(string.punctuation)}]""", '', t).strip()
            if temp != '':
                output.append(temp)
        return output


class LowercaseNormalizer(PyspaceNormalizer):

    defaults = {
        "lang": "EN",
    }

    def normalize_tokens(self, tokens):
        return [xNormalizer.lower(t, lang=self.component_config["lang"]) for t in tokens]
    
    def normalize_text(self, text):
        return xNormalizer.lower(text, lang=self.component_config["lang"])

class StopwordsNormalizer(PyspaceNormalizer):

    defaults = {
        "lang": "TR",
    }
    

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        super().__init__(component_config)
        # TODO
        # from pyspace_resources.stopwords.turkish import stopwords
        self.stopwords = stopwords

    def normalize_tokens(self, tokens):

        return [t for t in tokens if t not in self.stopwords]
    
