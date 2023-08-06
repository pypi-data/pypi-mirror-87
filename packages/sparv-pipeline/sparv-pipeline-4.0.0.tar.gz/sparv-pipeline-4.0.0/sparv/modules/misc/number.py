"""Annotators for numbering things."""

import random
import re
from binascii import hexlify
from collections import defaultdict

from sparv import Annotation, Output, Wildcard, annotator

START_DEFAULT = 1


@annotator("Number {annotation} by position", wildcards=[Wildcard("annotation", Wildcard.ANNOTATION)])
def number_by_position(out: Output = Output("{annotation}:misc.number_position"),
                       chunk: Annotation = Annotation("{annotation}"),
                       prefix: str = "",
                       zfill: bool = False,
                       start: int = START_DEFAULT):
    """Number chunks by their position."""
    spans = list(chunk.read_spans())

    def _order(index, _value):
        return spans[index]

    _read_chunks_and_write_new_ordering(out, chunk, _order, prefix, zfill, start)


@annotator("Number {annotation} randomly", wildcards=[Wildcard("annotation", Wildcard.ANNOTATION)])
def number_random(out: Output = Output("{annotation}:misc.number_random"),
                  chunk: Annotation = Annotation("{annotation}"),
                  prefix: str = "",
                  zfill: bool = False,
                  start: int = START_DEFAULT):
    """Number chunks randomly.

    Uses index as random seed.
    """
    def _order(index, _value):
        random.seed(int(hexlify(str(index).encode()), 16))
        return random.random()

    _read_chunks_and_write_new_ordering(out, chunk, _order, prefix, zfill, start)


@annotator("Number {annotation}, with the order determined by {attribute}", wildcards=[
    Wildcard("annotation", Wildcard.ANNOTATION),
    Wildcard("attribute", Wildcard.ATTRIBUTE)
])
def number_by_attribute(out: Output = Output("{annotation}:misc.number_by_{attribute}"),
                        chunk: Annotation = Annotation("{annotation}:{attribute}"),
                        prefix: str = "",
                        zfill: bool = False,
                        start: int = START_DEFAULT):
    """Number chunks, with the order determined by an attribute."""
    def _order(_index, value):
        return _natural_sorting(value)

    _read_chunks_and_write_new_ordering(out, chunk, _order, prefix, zfill, start)


@annotator("Renumber already numbered {annotation}:{attribute}, in new random order", wildcards=[
    Wildcard("annotation", Wildcard.ANNOTATION),
    Wildcard("attribute", Wildcard.ATTRIBUTE)
])
def renumber_by_shuffle(out: Output = Output("{annotation}:misc.renumber_by_shuffle_{attribute}"),
                        chunk: Annotation = Annotation("{annotation}:{attribute}"),
                        prefix: str = "",
                        zfill: bool = False,
                        start: int = START_DEFAULT):
    """Renumber already numbered chunks, in new random order.

    Retains the connection between parallelly numbered chunks by using the values as random seed.
    """
    def _order(_index, value):
        random.seed(int(hexlify(value.encode()), 16))
        return random.random(), _natural_sorting(value)

    _read_chunks_and_write_new_ordering(out, chunk, _order, prefix, zfill, start)


@annotator("Number {annotation} by ({parent_annotation}:{parent_attribute} order, {annotation} order)", wildcards=[
    Wildcard("annotation", Wildcard.ANNOTATION),
    Wildcard("parent_annotation", Wildcard.ANNOTATION),
    Wildcard("parent_attribute", Wildcard.ATTRIBUTE)
])
def number_by_parent(out: Output = Output("{annotation}:misc.number_by_parent_{parent_annotation}__{parent_attribute}"),
                     chunk: Annotation = Annotation("{annotation}"),
                     parent_order: Annotation = Annotation("{parent_annotation}:{parent_attribute}"),
                     prefix: str = "",
                     zfill: bool = False,
                     start: int = START_DEFAULT):
    """Number chunks by (parent_order, chunk order)."""
    parent_children, _orphans = parent_order.get_children(chunk)

    child_order = {child_index: (parent_nr, child_index)
                   for parent_index, parent_nr in enumerate(parent_order.read())
                   for child_index in parent_children[parent_index]}

    def _order(index, _value):
        return child_order.get(index)

    _read_chunks_and_write_new_ordering(out, chunk, _order, prefix, zfill, start)


@annotator("Number {annotation} by relative position within {parent}", wildcards=[
    Wildcard("annotation", Wildcard.ANNOTATION),
    Wildcard("parent", Wildcard.ANNOTATION)
])
def number_relative(out: Output = Output("{annotation}:misc.number_rel_{parent}"),
                    parent: Annotation = Annotation("{parent}"),
                    child: Annotation = Annotation("{annotation}"),
                    prefix: str = "",
                    zfill: bool = False,
                    start: int = START_DEFAULT):
    """Number chunks by their relative position within a parent."""
    parent_children, _orphans = parent.get_children(child)

    out.write(("{prefix}{nr:0{length}d}".format(prefix=prefix,
                                                length=len(str(len(parent) - 1 + start))
                                                if zfill else 0,
                                                nr=cnr)
               for parent in parent_children
               for cnr, _index in enumerate(parent, start)))


def _read_chunks_and_write_new_ordering(out: Output, chunk: Annotation, order, prefix="", zfill=False,
                                        start=START_DEFAULT):
    """Common function called by other numbering functions."""
    new_order = defaultdict(list)

    in_annotation = list(chunk.read())

    for i, val in enumerate(in_annotation):
        val = order(i, val)
        new_order[val].append(i)

    out_annotation = chunk.create_empty_attribute()

    nr_digits = len(str(len(new_order) - 1 + start))
    for nr, key in enumerate(sorted(new_order), start):
        for index in new_order[key]:
            out_annotation[index] = "{prefix}{nr:0{length}d}".format(prefix=prefix,
                                                                     length=nr_digits if zfill else 0,
                                                                     nr=nr)

    out.write(out_annotation)


def _natural_sorting(astr):
    """Convert a string into a naturally sortable tuple."""
    return tuple(int(s) if s.isdigit() else s for s in re.split(r"(\d+)", astr))
