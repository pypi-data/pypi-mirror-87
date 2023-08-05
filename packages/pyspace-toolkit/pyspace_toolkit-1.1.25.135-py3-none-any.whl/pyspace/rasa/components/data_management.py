import re
import os
from typing import Any, Dict, List, Optional, Text, Union, Type

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.components import Component
from rasa.nlu.featurizers.featurizer import SparseFeaturizer
from rasa.nlu.training_data import Message, TrainingData

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.constants import DOCS_URL_TRAINING_DATA_NLU
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

from rasa.nlu.config import RasaNLUModelConfig

import rasa.utils.io as io_utils
from rasa.nlu import utils
import rasa.utils.common as common_utils
from rasa.nlu.model import Metadata

import copy
import re

class TrainingDataManager:

    @staticmethod
    def apply_grouped_labels(training_data, intent_groups, intent_groups_prefix):
        
        raw_intents = [message.get(INTENT) for message in training_data.training_examples]

        for message in training_data.training_examples:
            intent = message.get(INTENT)
            for idx, group_i in enumerate(intent_groups):
                if intent in group_i:
                    if len(group_i) != 1:
                        message.set(INTENT, f'{intent_groups_prefix}{idx}')
                    break

        return raw_intents

    @staticmethod
    def recover_original_labels(training_data, raw_intents):
        for message, raw_intent in zip(training_data.training_examples, raw_intents):
            message.set(INTENT, raw_intent)

    @staticmethod
    def rename_labels(training_examples, regex_pattern, replace_pattern):
        for message in training_examples:
            intent = message.get(INTENT)
            updated_intent_name = re.sub(regex_pattern, replace_pattern, intent)
            message.set(INTENT, updated_intent_name)

    @staticmethod
    def filter_trainingdata(training_data, filter_intents):
        
        filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in filter_intents]
        # training_data.training_examples = filtered_training_examples
        return filtered_training_examples

        # filtered_training_examples = []
        # if filter_intents:
        #     filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) in filter_intents]
        # elif exclude_intents:
        #     filtered_training_examples = [e for e in training_data.training_examples if e.get(INTENT) not in exclude_intents]
        # else:
        #     assert "No filter intent or exlcude intent" == 0
        # return filtered_training_examples
        pass
    
    @staticmethod
    def generate_filter_intents_by_regex(training_data, regex=''):
        
        # exclude pattern
        # '^(account_tr|bill_payment_tr)$'
        # '^((?!account_tr).)*$'
        # '^((?!(badword|one)).)*$'

        filter_intents = []
        all_intents = list(set([e.get(INTENT) for e in training_data.training_examples]))
        for intent in all_intents:
            if re.findall(regex, intent):
                filter_intents.append(intent)

        return filter_intents

    @staticmethod
    def generate_filter_intents_by_exclude_intents(training_data, exclude_intents=[]):
        filter_intents = []
        all_intents = list(set([e.get(INTENT) for e in training_data.training_examples]))
        for intent in all_intents:
            if intent not in exclude_intents:
                filter_intents.append(intent)

        return filter_intents
    



class BackupRawData(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        training_data.raw_data = copy.deepcopy(training_data.training_examples)

class BackupFeatures(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        features = self.component_config["features"]
        for message in training_data.training_examples:
            for feature in features:
                message.set(f"backup_{feature}", message.get(feature))

    def process(self, message: Message, **kwargs: Any) -> None:
        features = self.component_config["features"]
        for feature in features:
            message.set(f"backup_{feature}", message.get(feature))

class RecoverFeatures(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):

        features = self.component_config["features"]
        for message in training_data.training_examples:
            for feature in features:
                message.set(feature, message.get(f"backup_{feature}"))
                if feature == 'text':
                    message.text = message.get(f"backup_{feature}")

    def process(self, message: Message, **kwargs: Any) -> None:
        features = self.component_config["features"]
        for feature in features:
            message.set(feature, message.get(f"backup_{feature}"))
            if feature == 'text':
                message.text = message.get(f"backup_{feature}")


class LoadData(Component):

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        dataset = self.component_config["partition_name"]
        training_data.training_examples = getattr(training_data, dataset)
        
class PartitionData(Component):

    defaults = {
        "partition_intents":[],
        "partition_mode": 'select', # exclude, regex
        "partition_name": 'post_classification',
        "rename_intents": False,
    }

    def train(self, training_data: TrainingData, config: Optional[RasaNLUModelConfig] = None, **kwargs: Any,):
        assert self.component_config["partition_name"] not in ['training_examples', 'raw_data']

        if self.component_config["partition_mode"]=='select':
            filter_intents = self.component_config["partition_intents"]
        elif self.component_config["partition_mode"]=='exclude':
            filter_intents = TrainingDataManager.generate_filter_intents_by_exclude_intents(training_data, self.component_config["partition_intents"])
        elif self.component_config["partition_mode"]=='regex':
            filter_intents = TrainingDataManager.generate_filter_intents_by_regex(training_data, self.component_config["partition_intents"])
        else:
            assert 'Partition mode is not allowed.'

        partition_training_examples = TrainingDataManager.filter_trainingdata(training_data, filter_intents)

        if self.component_config["rename_intents"] is not False:
            TrainingDataManager.rename_labels(partition_training_examples, *self.component_config["rename_intents"])

        setattr(training_data, self.component_config["partition_name"], partition_training_examples)
