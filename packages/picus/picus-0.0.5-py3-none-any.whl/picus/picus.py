#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from picus import __version__
from picus.core.variantclassification import VariantClassification
from picus.core.evidencecollection import EvidenceCollection

import pandas as pd


def get_args():
    parser = argparse.ArgumentParser()

    # Not functional
    parser.add_argument('-v', '--verbose', required=False, action='store_true',
                        help='WIP.Write what is happening to stdout.')

    parser.add_argument('--version',
                        action='version', version=__version__)

    parser.add_argument('-i', '--input', required=True,
                        default=None, type=str, help='input annotation file.')
    parser.add_argument('-o', '--output', required=False,
                        default=None, type=str, help='output annotation file.')

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    input_file = args.input
    output_file = args.output
    variant_info_cols = [
        'CHR', 'POS', 'REF', 'ALT', 'GT', 'AD',
        'id', 'gene_symbol', 'transcript_id',
        'hgvsc', 'hgvsp',
        'transcript_consequence_terms',
        'evidences', 'significance'
    ]

    df = pd.read_csv(
        input_file,
        dtype={'CHR': 'object'},
        low_memory=False,
    )
    evidence_collector = EvidenceCollection()
    variant_classifier = VariantClassification()

    df = evidence_collector.collect_evidences(df)

    df['significance'] = df.evidences.apply(
        variant_classifier.classify_variant,
        args=(True,)
    )
    df['evidences'] = df.evidences.apply(
        evidence_collector.flat_evidences
    )

    if output_file is None:
        sys.stdout.write(
            df[variant_info_cols].to_json(orient='records')
        )
    else:
        if output_file.endswith('.csv'):
            df.to_csv(output_file, index=False)


if __name__ == '__main__':
    main()
