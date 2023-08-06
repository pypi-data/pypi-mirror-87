from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg
import re
import numpy as np


class SpanishPluralAbbreviations(NormalizerBase):
    DESCRIPTION_TRAINING = """
            Normalizes the plural abbreviations in Spanish following its rules.
        """

    DESCRIPTION_DECODING = """
            
        """

    NAME = "spanish_plural_abbreviations"


    SPACES = ["\u0020", "\u2000", "\u2001", "\u2002", "\u2003", "\u2004", "\u2005", "\u2006", "\u2007", "\u2008", "\u2009",
          "\u200A", "\u202F", "\u205F", "\u3000"]

    def __init__(self, src_lang: str, tgt_lang: str):
        super().__init__(src_lang, tgt_lang)

    def _index_of_the_space_of_the_plural_abbreviations(self, text):
        res_text = []
        iterator = re.finditer(r'([A-Z])\1[\.\s]{1,2}[A-Z]{2}', text)
        for character in iterator:
            plural_abbreviation = character.group(0)
            aux = text.index(plural_abbreviation[0]) + 3
            res_text.append(aux)
        res_text = np.array(res_text)
        return res_text

    def _is_abbreviation_at_the_end(self, text, index_of_the_space):
        index_of_the_end = index_of_the_space + 3
        for index in index_of_the_end:
            if index >= len(text):
                return True
        return False

    def _normalize(self, text):
        """Correct the plural abbreviations"""
        res_text = []
        index_of_the_space = self._index_of_the_space_of_the_plural_abbreviations(text)
        abbreviation_at_the_end = self._is_abbreviation_at_the_end(text, index_of_the_space)
        index_of_the_dot = index_of_the_space + 2
        i = 0
        j = 0
        for i in range(len(text)): #while i <= len(text) - 1:
            if i in index_of_the_space:
                res_text.append("\u00A0")  # Unicode non-breaking space
                if text[i] not in self.SPACES:
                    res_text.append(text[i])
                else:
                    index_of_the_dot[j] += 1
                j += 1
                i += 1
            elif i in index_of_the_dot:
                if text[i] == ".":
                    res_text.append(text[i])
                else:
                    res_text.append(".")
                    res_text.append(text[i])
                i += 1
            else:
                res_text.append(text[i])
                i += 1
                if i == len(text) and abbreviation_at_the_end:
                    res_text.append(".")
        return "".join(res_text)

    # Called when training
    def process_train(self, seg: Seg) -> None:
        if self.get_src_lang() == "es":
            seg.src = self._normalize(seg.src)
        if seg.tgt is not None and self.get_tgt_lang() == "es":
            seg.tgt = self._normalize(seg.tgt)

    # Called when using model (before calling model to translate)
    def process_src_decoding(self, seg: Seg) -> None:
        if self.get_src_lang() == "es":
            seg.src = self._normalize(seg.src)

    # Called after the model translated (in case this would be necessary; usually not the case)
    def process_tgt_decoding(self, seg: Seg) -> None:
        if self.get_tgt_lang() == "es":
            seg.tgt = self._normalize(seg.tgt)
