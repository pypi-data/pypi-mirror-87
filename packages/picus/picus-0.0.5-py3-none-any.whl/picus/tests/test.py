from pathlib import Path
import sys
from dove.utils.vcf import Vcf
sys.path.append(Path(__file__).resolve().parent.parent.as_posix())
from core.evidencecollection import EvidenceCollection
from core.variantclassification import VariantClassification


with Vcf('test.vcf.gz') as f:
    f.vdf['CSQ'] = f.get_variant_info(concat=True, drop=True)['CSQ']
    f.vdf = f.get_sample_format(concat=True, drop=True)
    vep_header = [i for i in f.meta_info['INFO'] if 'CSQ' in i][0].split('Format: ')[
        1].strip('">').split('|')
    f.vdf.CSQ = f.vdf.CSQ.str.split(',')
    df = f.vdf.explode('CSQ')

df[vep_header] = df.CSQ.str.split('|', expand=True)
df.drop(['INFO', 'CSQ'], axis=1, inplace=True)

evidence_collector = EvidenceCollection()
variant_classifier = VariantClassification()

import pandas as pd

df['gnomAD_AF'] = pd.to_numeric(df['gnomAD_AF'], errors="coerce")
df['AF'] = pd.to_numeric(df['AF'], errors="coerce")
df = evidence_collector.collect_evidences(df)
df['significance'] = df.evidences.apply(
    variant_classifier.classify_variant,
    args=(True,)
)
df['evidences'] = df.evidences.apply(
    evidence_collector.flat_evidences
)
