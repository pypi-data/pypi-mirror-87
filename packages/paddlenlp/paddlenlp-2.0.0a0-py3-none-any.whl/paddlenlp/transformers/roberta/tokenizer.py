# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from .. import BasicTokenizer, PretrainedTokenizer, WordpieceTokenizer

__all__ = ['RobertaTokenizer', ]


class RobertaTokenizer(PretrainedTokenizer):
    """
    Constructs a RoBERTa tokenizer. It uses a basic tokenizer to do punctuation
    splitting, lower casing and so on, and follows a WordPiece tokenizer to
    tokenize as subwords.
    Args:
        vocab_file (str): file path of the vocabulary
        do_lower_case (bool): Whether the text strips accents and convert to
            lower case. Default: `True`.
            Default: True.
        unk_token (str): The special token for unkown words. Default: "[UNK]".
        sep_token (str): The special token for separator token . Default: "[SEP]".
        pad_token (str): The special token for padding. Default: "[PAD]".
        cls_token (str): The special token for cls. Default: "[CLS]".
        mask_token (str): The special token for mask. Default: "[MASK]".
    
    Examples:
        .. code-block:: python
            from paddlenlp.transformers import RobertaTokenizer
            tokenizer = RobertaTokenizer.from_pretrained('bert-base-uncased')
            # the following line get: ['he', 'was', 'a', 'puppet', '##eer']
            tokens = tokenizer('He was a puppeteer')
            # the following line get: 'he was a puppeteer'
            tokenizer.convert_tokens_to_string(tokens)
    """
    resource_files_names = {"vocab_file": "vocab.txt"}  # for save_pretrained
    pretrained_resource_files_map = {
        "vocab_file": {
            "roberta-wwm-ext":
            "https://paddlenlp.bj.bcebos.com/models/transformers/roberta_base/vocab.txt",
            "roberta-wwm-ext-large":
            "https://paddlenlp.bj.bcebos.com/models/transformers/roberta_large/vocab.txt",
            "rbt3":
            "https://paddlenlp.bj.bcebos.com/models/transformers/rbt3/vocab.txt",
            "rbtl3":
            "https://paddlenlp.bj.bcebos.com/models/transformers/rbtl3/vocab.txt",
        }
    }
    pretrained_init_configuration = {
        "roberta-wwm-ext": {
            "do_lower_case": True
        },
        "roberta-wwm-ext-large": {
            "do_lower_case": True
        },
        "rbt3": {
            "do_lower_case": True
        },
        "rbtl3": {
            "do_lower_case": True
        },
    }

    def __init__(self,
                 vocab_file,
                 do_lower_case=True,
                 unk_token="[UNK]",
                 sep_token="[SEP]",
                 pad_token="[PAD]",
                 cls_token="[CLS]",
                 mask_token="[MASK]"):

        if not os.path.isfile(vocab_file):
            raise ValueError(
                "Can't find a vocabulary file at path '{}'. To load the "
                "vocabulary from a pretrained model please use "
                "`tokenizer = RobertaTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)`"
                .format(vocab_file))
        self.vocab = self.load_vocabulary(vocab_file, unk_token=unk_token)
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case)
        self.wordpiece_tokenizer = WordpieceTokenizer(
            vocab=self.vocab, unk_token=unk_token)

    @property
    def vocab_size(self):
        """
        return the size of vocabulary.
        Returns:
            int: the size of vocabulary.
        """
        return len(self.vocab)

    def _tokenize(self, text):
        """
        End-to-end tokenization for RoBERTa models.
        Args:
            text (str): The text to be tokenized.
        
        Returns:
            list: A list of string representing converted tokens.
        """
        split_tokens = []
        for token in self.basic_tokenizer.tokenize(text):
            for sub_token in self.wordpiece_tokenizer.tokenize(token):
                split_tokens.append(sub_token)
        return split_tokens

    def __call__(self, text):
        """
        End-to-end tokenization for RoBERTa models.
        Args:
            text (str): The text to be tokenized.
        
        Returns:
            list: A list of string representing converted tokens.
        """
        return self._tokenize(text)

    def convert_tokens_to_string(self, tokens):
        """
        Converts a sequence of tokens (list of string) in a single string. Since
        the usage of WordPiece introducing `##` to concat subwords, also remove
        `##` when converting.
        Args:
            tokens (list): A list of string representing tokens to be converted.
        Returns:
            str: Converted string from tokens.
        """
        out_string = " ".join(tokens).replace(" ##", "").strip()
        return out_string
