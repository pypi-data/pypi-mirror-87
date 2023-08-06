"""Annotate text chunks with lexical classes from Blingbring or SweFN."""

import logging
from collections import defaultdict
from typing import Optional

import sparv.util as util
from sparv import Annotation, Config, Model, Output, annotator

log = logging.getLogger(__name__)


@annotator("Annotate text chunks with Blingbring classes", language=["swe"], config=[
    Config("lexical_classes.bb_freq_model", default="lexical_classes/blingbring.freq.gp2008+suc3+romi.pickle",
           description="Path to Blingbring frequency model")
])
def blingbring_text(out: Output = Output("<text>:lexical_classes.blingbring",
                                         description="Lexical classes for text chunks from Blingbring"),
                    lexical_classes_token: Annotation = Annotation("<token>:lexical_classes.blingbring"),
                    text: Annotation = Annotation("<text>"),
                    token: Annotation = Annotation("<token>"),
                    saldoids: Optional[Annotation] = Annotation("<token:sense>"),
                    cutoff: int = 3,
                    types: bool = False,
                    delimiter: str = util.DELIM,
                    affix: str = util.AFFIX,
                    freq_model: Model = Model("[lexical_classes.bb_freq_model]"),
                    decimals: int = 3):
    """Annotate text chunks with Blingbring classes."""
    annotate_text(out=out, lexical_classes_token=lexical_classes_token, text=text, token=token,
                  saldoids=saldoids, cutoff=cutoff, types=types, delimiter=delimiter, affix=affix,
                  freq_model=freq_model, decimals=decimals)


@annotator("Annotate text chunks with SweFN classes", language=["swe"], config=[
    Config("lexical_classes.swefn_freq_model", default="lexical_classes/swefn.freq.gp2008+suc3+romi.pickle",
           description="Path to SweFN frequency model")
])
def swefn_text(out: Output = Output("<text>:lexical_classes.swefn",
                                    description="Lexical classes for text chunks from SweFN"),
               lexical_classes_token: Annotation = Annotation("<token>:lexical_classes.swefn"),
               text: Annotation = Annotation("<text>"),
               token: Annotation = Annotation("<token>"),
               saldoids: Optional[Annotation] = Annotation("<token:sense>"),
               cutoff: int = 3,
               types: bool = False,
               delimiter: str = util.DELIM,
               affix: str = util.AFFIX,
               freq_model: Model = Model("[lexical_classes.swefn_freq_model]"),
               decimals: int = 3):
    """Annotate text chunks with SweFN classes."""
    annotate_text(out=out, lexical_classes_token=lexical_classes_token, text=text, token=token,
                  saldoids=saldoids, cutoff=cutoff, types=types, delimiter=delimiter, affix=affix,
                  freq_model=freq_model, decimals=decimals)


def annotate_text(out: Output, lexical_classes_token: Annotation, text: Annotation, token: Annotation,
                  saldoids, cutoff, types, delimiter, affix, freq_model, decimals):
    """
    Annotate text chuncs with lexical classes.

    - out: resulting annotation file
    - lexical_classes_token: existing annotation with lexical classes on token level.
    - text, token: existing annotations for the text-IDs and the tokens.
    - saldoids: existing annotation with saldoIDs, needed when types=True.
    - cutoff: value for limiting the resulting bring classes.
              The result will contain all words with the top x frequencies.
              Words with frequency = 1 will be removed from the result.
    - types: if True, count every class only once per saldo ID occurrence.
    - delimiter: delimiter character to put between ambiguous results.
    - affix: optional character to put before and after results to mark a set.
    - freq_model: pickled file with reference frequencies.
    - decimals: number of decimals to keep in output.
    """
    cutoff = int(cutoff)
    text_children, _orphans = text.get_children(token, preserve_parent_annotation_order=True)
    classes = list(lexical_classes_token.read())
    sense = list(saldoids.read()) if types else None

    if freq_model:
        freq_model = util.PickledLexicon(freq_model.path)

    out_annotation = text.create_empty_attribute()

    for text_index, words in enumerate(text_children):
        seen_types = set()
        class_freqs = defaultdict(int)

        for token_index in words:
            # Count only sense types
            if types:
                senses = str(sorted([s.split(util.SCORESEP)[0] for s in sense[token_index].strip(util.AFFIX).split(util.DELIM)]))
                if senses in seen_types:
                    continue
                else:
                    seen_types.add(senses)

            rogwords = classes[token_index].strip(util.AFFIX).split(util.DELIM) if classes[token_index] != util.AFFIX else []
            for w in rogwords:
                class_freqs[w] += 1

        if freq_model:
            for c in class_freqs:
                # Relative frequency
                rel = class_freqs[c] / len(words)
                # Calculate class dominance
                ref_freq = freq_model.lookup(c.replace("_", " "), 0)
                if not ref_freq:
                    log.error("Class '%s' is missing" % ref_freq)
                class_freqs[c] = (rel / ref_freq)

        # Sort words according to frequency/dominance
        ordered_words = sorted(class_freqs.items(), key=lambda x: x[1], reverse=True)
        if freq_model:
            # Remove words with dominance < 1
            ordered_words = [w for w in ordered_words if w[1] >= 1]
        else:
            # Remove words with frequency 1
            ordered_words = [w for w in ordered_words if w[1] > 1]

        if len(ordered_words) > cutoff:
            cutoff_freq = ordered_words[cutoff - 1][1]
            ordered_words = [w for w in ordered_words if w[1] >= cutoff_freq]

        # Join words and frequencies/dominances
        ordered_words = [util.SCORESEP.join([word, str(round(freq, decimals))]) for word, freq in ordered_words]
        out_annotation[text_index] = util.cwbset(ordered_words, delimiter, affix) if ordered_words else affix

    out.write(out_annotation)
