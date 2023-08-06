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
import pickle
import six
import shutil

from paddle.utils import try_import
from paddlenlp.utils.env import MODEL_HOME

from .. import BasicTokenizer, PretrainedTokenizer, WordpieceTokenizer

__all__ = ['ErnieTokenizer', 'ErnieTinyTokenizer']


class ErnieTokenizer(PretrainedTokenizer):
    """
    Constructs an ERNIE tokenizer. It uses a basic tokenizer to do punctuation
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
            from paddlenlp.transformers import ErnieTokenizer
            tokenizer = ErnieTokenizer.from_pretrained('ernie')
            # the following line get: ['he', 'was', 'a', 'puppet', '##eer']
            tokens = tokenizer('He was a puppeteer')
            # the following line get: 'he was a puppeteer'
            tokenizer.convert_tokens_to_string(tokens)
    """
    resource_files_names = {"vocab_file": "vocab.txt"}  # for save_pretrained
    pretrained_resource_files_map = {
        "vocab_file": {
            "ernie":
            "https://paddlenlp.bj.bcebos.com/models/transformers/ernie/vocab.txt",
            "ernie_v2_eng_base":
            "https://paddlenlp.bj.bcebos.com/models/transformers/ernie_v2_base/vocab.txt",
            "ernie_v2_eng_large":
            "https://paddlenlp.bj.bcebos.com/models/transformers/ernie_v2_large/vocab.txt",
        }
    }
    pretrained_init_configuration = {
        "ernie": {
            "do_lower_case": True
        },
        "ernie_v2_eng_base": {
            "do_lower_case": True
        },
        "ernie_v2_eng_large": {
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
                "`tokenizer = ErnieTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)`"
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
        End-to-end tokenization for ERNIE models.
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
        End-to-end tokenization for ERNIE models.
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


class ErnieTinyTokenizer(PretrainedTokenizer):
    """
    Constructs a ErnieTiny tokenizer. It uses the `dict.wordseg.pickle` cut the text to words, and 
    use the `sentencepiece` tools to cut the words to sub-words. 
    Args:
        vocab_file (str): file path of the vocabulary
        do_lower_case (bool): Whether the text strips accents and convert to
            lower case. Default: `True`.
        unk_token (str): The special token for unkown words. Default: "[UNK]".
        sep_token (str): The special token for separator token . Default: "[SEP]".
        pad_token (str): The special token for padding. Default: "[PAD]".
        cls_token (str): The special token for cls. Default: "[CLS]".
        mask_token (str): The special token for mask. Default: "[MASK]".
    
    Examples:
        .. code-block:: python
            from paddlenlp.transformers import ErnieTinyTokenizer
            tokenizer = ErnieTinyTokenizer.from_pretrained('ernie_tiny)
            # the following line get: ['he', 'was', 'a', 'puppet', '##eer']
            tokens = tokenizer('He was a puppeteer')
            # the following line get: 'he was a puppeteer'
            tokenizer.convert_tokens_to_string(tokens)
    """
    resource_files_names = {
        "sentencepiece_model_file": "spm_cased_simp_sampled.model",
        "vocab_file": "vocab.txt",
        "word_dict": "dict.wordseg.pickle"
    }  # for save_pretrained
    pretrained_resource_files_map = {
        "vocab_file": {
            "ernie_tiny":
            "https://paddlenlp.bj.bcebos.com/models/transformers/ernie_tiny/vocab.txt"
        },
        "sentencepiece_model_file": {
            "ernie_tiny":
            "https://paddlenlp.bj.bcebos.com/models/transformers/ernie_tiny/spm_cased_simp_sampled.model"
        },
        "word_dict": {
            "ernie_tiny":
            "https://paddlenlp.bj.bcebos.com/models/transformers/ernie_tiny/dict.wordseg.pickle"
        },
    }
    pretrained_init_configuration = {"ernie_tiny": {"do_lower_case": True}}

    def __init__(self,
                 vocab_file,
                 sentencepiece_model_file,
                 word_dict,
                 do_lower_case=True,
                 encoding="utf8",
                 unk_token="[UNK]",
                 sep_token="[SEP]",
                 pad_token="[PAD]",
                 cls_token="[CLS]",
                 mask_token="[MASK]"):
        mod = try_import('sentencepiece')
        self.sp_model = mod.SentencePieceProcessor()
        self.word_dict = word_dict

        self.do_lower_case = do_lower_case
        self.encoding = encoding
        if not os.path.isfile(vocab_file):
            raise ValueError(
                "Can't find a vocabulary file at path '{}'. To load the "
                "vocabulary from a pretrained model please use "
                "`tokenizer = ErnieTinyTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)`"
                .format(vocab_file))
        if not os.path.isfile(word_dict):
            raise ValueError(
                "Can't find a file at path '{}'. To load the "
                "word dict from a pretrained model please use "
                "`tokenizer = ErnieTinyTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)`"
                .format(word_dict))
        self.dict = pickle.load(open(word_dict, 'rb'))
        self.vocab = self.load_vocabulary(vocab_file, unk_token=unk_token)

        # if the sentencepiece_model_file is not exists, just the default sentence-piece model 
        if os.path.isfile(sentencepiece_model_file):
            self.sp_model.Load(sentencepiece_model_file)

    @property
    def vocab_size(self):
        """
        return the size of vocabulary.
        Returns:
            int: the size of vocabulary.
        """
        return len(self.vocab)

    def cut(self, chars):
        words = []
        idx = 0
        window_size = 5
        while idx < len(chars):
            matched = False

            for i in range(window_size, 0, -1):
                cand = chars[idx:idx + i]
                if cand in self.dict:
                    words.append(cand)
                    matched = True
                    break
            if not matched:
                i = 1
                words.append(chars[idx])
            idx += i
        return words

    def _tokenize(self, text):
        """
        End-to-end tokenization for ErnieTiny models.
        Args:
            text (str): The text to be tokenized.
        
        Returns:
            list: A list of string representing converted tokens.
        """
        if len(text) == 0:
            return []
        if not isinstance(text, six.string_types):
            text = text.decode(self.encoding)

        text = [s for s in self.cut(text) if s != ' ']
        text = ' '.join(text)
        text = text.lower()

        tokens = self.sp_model.EncodeAsPieces(text)
        in_vocab_tokens = []
        unk_token = self.vocab.unk_token
        for token in tokens:
            if token in self.vocab:
                in_vocab_tokens.append(token)
            else:
                in_vocab_tokens.append(unk_token)
        return in_vocab_tokens

    def __call__(self, text):
        """
        End-to-end tokenization for ERNIE Tiny models.
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

    def save_resources(self, save_directory):
        """
        Save tokenizer related resources to files under `save_directory`.
        Args:
            save_directory (str): Directory to save files into.
        """
        for name, file_name in self.resource_files_names.items():
            ### TODO: make the name 'ernie_tiny' as a variable
            source_path = os.path.join(MODEL_HOME, 'ernie_tiny', file_name)
            save_path = os.path.join(save_directory,
                                     self.resource_files_names[name])
            shutil.copyfile(source_path, save_path)
