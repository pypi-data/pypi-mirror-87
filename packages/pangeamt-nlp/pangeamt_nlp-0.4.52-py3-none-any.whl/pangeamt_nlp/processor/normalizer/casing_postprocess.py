from pangeamt_nlp.processor.base.normalizer_base import NormalizerBase
from pangeamt_nlp.seg import Seg, SegCase
from sacremoses import MosesDetruecaser


class CasingPostprocess(NormalizerBase):
    NAME = "casing_postprocess"

    DESCRIPTION_TRAINING = """"""

    DESCRIPTION_DECODING = """
        Copy the casing of the source
    """

    def __init__(self, src_lang: str, tgt_lang: str) -> None:
        super().__init__(src_lang, tgt_lang)
        self._detruecaser = MosesDetruecaser()
        self._comillas = ["'", '"', "‘", '«', "“", '「', '『','„', '»', '›', '‚', '‹']

    def process_train(self, seg: Seg) -> None:
        pass

    def process_src_decoding(self, seg: Seg) -> None:
        if seg.src_raw.isupper():
            seg.src = seg.src.lower()

    def process_tgt_decoding(self, seg: Seg) -> None:
        if seg.src_raw != '' and seg.src_raw != '\n' and seg.src_raw != ""\
                and seg.tgt != '' and seg.tgt != '\n' and seg.tgt != "":
            if seg.src_case == SegCase.UPPER:
                seg.tgt = seg.tgt.upper()
            elif seg.src_case == SegCase.LOWER:
                seg.tgt = seg.tgt.lower()
            elif seg.src_case == SegCase.MIXED:
                if seg.src[0] not in self._comillas:
                    if seg.src_raw[0].isupper():
                        seg.tgt = (" ").join(self._detruecaser.detruecase(seg.tgt))
                    elif seg.src_raw[0].islower():
                        seg.tgt = (" ").join(self._detruecaser.detruecase(seg.tgt))
                    seg.tgt = seg.tgt
                else:
                    if seg.src_raw[1].isupper():
                        if seg.tgt[0] in self._comillas:
                            seg.tgt = seg.tgt[0] + seg.tgt[1].upper() + seg.tgt[2:]
                        else:
                            seg.tgt = (" ").join(self._detruecaser.detruecase(seg.tgt))
                    elif seg.src_raw[1].islower():
                        if seg.tgt[0] in self._comillas:
                            seg.tgt = seg.tgt[0] + seg.tgt[1].lower() + seg.tgt[2:]
                        else:
                            seg.tgt = (" ").join(self._detruecaser.detruecase(seg.tgt))
                    seg.tgt = seg.tgt

