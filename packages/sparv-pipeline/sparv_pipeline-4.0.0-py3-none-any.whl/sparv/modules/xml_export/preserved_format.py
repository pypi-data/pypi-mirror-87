"""Export annotated corpus data to format-preserved xml."""

import logging
import os
import xml.etree.ElementTree as etree

import sparv.util as util
from sparv import (AnnotationData, Config, Document, Export, ExportAnnotations, SourceAnnotations, Text, exporter)
from . import xml_utils

log = logging.getLogger(__name__)


@exporter("XML export preserving whitespaces from source file", config=[
    Config("xml_export.filename_formatted", default="{doc}_export.xml",
           description="Filename pattern for resulting XML files, with '{doc}' representing the source name.")
])
def preserved_format(doc: Document = Document(),
                     text: Text = Text(),
                     docid: AnnotationData = AnnotationData("<docid>"),
                     out: Export = Export("xml_preserved_format/[xml_export.filename_formatted]"),
                     annotations: ExportAnnotations = ExportAnnotations("xml_export.annotations"),
                     source_annotations: SourceAnnotations = SourceAnnotations("xml_export.source_annotations"),
                     header_annotations: SourceAnnotations = SourceAnnotations("xml_export.header_annotations"),
                     remove_namespaces: bool = Config("export.remove_module_namespaces", False),
                     sparv_namespace: str = Config("export.sparv_namespace"),
                     source_namespace: str = Config("export.source_namespace"),
                     include_empty_attributes: bool = Config("xml_export.include_empty_attributes")):
    """Export annotations to XML in export_dir and keep whitespaces and indentation from original file.

    Args:
        doc: Name of the original document.
        text: The corpus text.
        docid: Annotation with document IDs.
        out: Path and filename pattern for resulting file.
        annotations: List of elements:attributes (annotations) to include.
        source_annotations: List of elements:attributes from the original document
            to be kept. If not specified, everything will be kept.
        header_annotations: List of header elements from the original document to include
            in the export. If not specified, all headers will be kept.
        remove_namespaces: Whether to remove module "namespaces" from element and attribute names.
            Disabled by default.
        sparv_namespace: The namespace to be added to all Sparv annotations.
        source_namespace: The namespace to be added to all annotations present in the source.
        include_empty_attributes: Whether to include attributes even when they are empty. Disabled by default.
    """
    # Create export dir
    os.makedirs(os.path.dirname(out), exist_ok=True)

    # Read corpus text and document ID
    corpus_text = text.read()
    docid = docid.read()

    # Get annotation spans, annotations list etc.
    annotation_list, _, export_names = util.get_annotation_names(annotations, source_annotations, doc=doc,
                                                                 remove_namespaces=remove_namespaces,
                                                                 sparv_namespace=sparv_namespace,
                                                                 source_namespace=source_namespace)
    h_annotations, h_export_names = util.get_header_names(header_annotations, doc=doc)
    export_names.update(h_export_names)
    span_positions, annotation_dict = util.gather_annotations(annotation_list, export_names, h_annotations, doc=doc,
                                                              flatten=False, split_overlaps=True)
    sorted_positions = [(pos, span[0], span[1]) for pos, spans in sorted(span_positions.items()) for span in spans]

    # Root tag sanity check
    if not xml_utils.valid_root(sorted_positions[0], sorted_positions[-1]):
        raise util.SparvErrorMessage("Root tag is missing! If you have manually specified which elements to include, "
                                     "make sure to include an element that encloses all other included elements and "
                                     "text content.")

    # Create root node
    root_span = sorted_positions[0][2]
    root_span.set_node()
    node_stack = []
    last_pos = 0  # Keeps track of the position of the processed text

    for x, (_pos, instruction, span) in enumerate(sorted_positions):
        # Open node: Create child node under the top stack node
        if instruction == "open":
            # Set tail for previous node if necessary
            if last_pos < span.start:
                # Get last closing node in this position
                _, tail_span = [i for i in span_positions[last_pos] if i[0] == "close"][-1]
                tail_span.node.tail = corpus_text[last_pos:span.start]
                last_pos = span.start

            # Handle headers
            if span.is_header:
                header = annotation_dict[span.name][util.HEADER_CONTENTS][span.index]
                header_xml = etree.fromstring(header)
                header_xml.tag = span.export  # Rename element if needed
                span.node = header_xml
                node_stack[-1].node.append(header_xml)
            else:
                if node_stack:  # Don't create root node, it already exists
                    span.set_node(parent_node=node_stack[-1].node)

                xml_utils.add_attrs(span.node, span.name, annotation_dict, export_names, span.index,
                                    include_empty_attributes)
                if span.overlap_id:
                    if sparv_namespace:
                        span.node.set(f"{sparv_namespace}.{util.OVERLAP_ATTR}", f"{docid}-{span.overlap_id}")
                    else:
                        span.node.set(f"{util.SPARV_DEFAULT_NAMESPACE}.{util.OVERLAP_ATTR}",
                                      f"{docid}-{span.overlap_id}")
                node_stack.append(span)

                # Set text if there should be any between this node and the next one
                next_item = sorted_positions[x + 1]
                if next_item[1] == "open" and next_item[2].start > span.start:
                    span.node.text = corpus_text[last_pos:next_item[2].start]
                    last_pos = next_item[2].start

        # Close node
        else:
            if span.is_header:
                continue
            if last_pos < span.end:
                # Set node text if necessary
                if span.start == last_pos:
                    span.node.text = corpus_text[last_pos:span.end]
                # Set tail for previous node if necessary
                else:
                    # Get last closing node in this position
                    _, tail_span = [i for i in span_positions[last_pos] if i[0] == "close"][-1]
                    tail_span.node.tail = corpus_text[last_pos:span.end]
                last_pos = span.end

            # Make sure closing node == top stack node
            assert span == node_stack[-1], "Overlapping elements found: {}".format(node_stack[-2:])
            # Pop stack and move on to next span
            node_stack.pop()

    # Write xml to file
    etree.ElementTree(root_span.node).write(out, encoding="unicode", method="xml", xml_declaration=True)
    log.info("Exported: %s", out)
