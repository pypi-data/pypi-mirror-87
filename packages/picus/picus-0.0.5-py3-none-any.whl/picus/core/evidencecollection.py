# coding: utf-8

'''
# Criteria

## Pathogenic

### Pathogenic Very Strong
* PVS1 null variant (nonsense, frameshift, canonical ±1 or 2 splice sites, initiation codon, single or multiexon deletion) in a gene where LOF is a known mechanism of disease

### Pathogenic Strong
* PS1 Same amino acid change as a previously established pathogenic variant regardless of nucleotide change
* PS2 De novo (both maternity and paternity confirmed) in a patient with the disease and no family history
* PS3 Well-established in vitro or in vivo functional studies supportive of a damaging effect on the gene or gene product
* PS4 The prevalence of the variant in affected individuals is significantly increased compared with the prevalence in controls

### Pathogenic Moderate
* PM1 Located in a mutational hot spot and/or critical and well-established functional domain (e.g., active site of an enzyme) without benign variation
* PM2 Absent from controls (or at extremely low frequency if recessive) (Table 6) in Exome Sequencing Project, 1000 Genomes Project, or Exome Aggregation Consortium
* PM3 For recessive disorders, detected in trans with a pathogenic variant
* PM4 Protein length changes as a result of in-frame deletions/insertions in a nonrepeat region or stop-loss variants
* PM5 Novel missense change at an amino acid residue where a different missense change determined to be pathogenic has been seen before
* PM6 Assumed de novo, but without confirmation of paternity and maternity

### Pathogenic Supporting
* PP1 Cosegregation with disease in multiple affected family members in a gene definitively known to cause the disease
* PP2 Missense variant in a gene that has a low rate of benign missense variation and in which missense variants are a common mechanism of disease
* PP3 Multiple lines of computational evidence support a deleterious effect on the gene or gene product (conservation, evolutionary, splicing impact, etc.)
* PP4 Patient’s phenotype or family history is highly specific for a disease with a single genetic etiology
* PP5 Reputable source recently reports variant as pathogenic, but the evidence is not available to the laboratory to perform an independent evaluation

## Benign

### Benign Stand-alone
* BA1 Allele frequency is >5% in Exome Sequencing Project, 1000 Genomes Project, or Exome Aggregation Consortium

### Benign Strong
* BS1 Allele frequency is greater than expected for disorder
* BS2 Observed in a healthy adult individual for a recessive (homozygous), dominant (heterozygous), or X-linked (hemizygous) disorder, with full penetrance expected at an early age
* BS3 Well-established in vitro or in vivo functional studies show no damaging effect on protein function or splicing
* BS4 Lack of segregation in affected members of a family

### Benign Supporting
* BP1 Missense variant in a gene for which primarily truncating variants are known to cause disease
* BP2 Observed in trans with a pathogenic variant for a fully penetrant dominant gene/disorder or observed in cis with a pathogenic variant in any inheritance pattern
* BP3 In-frame deletions/insertions in a repetitive region without a known function
* BP4 Multiple lines of computational evidence suggest no impact on gene or gene product (conservation, evolutionary, splicing impact, etc.)
* BP5 Variant found in a case with an alternate molecular basis for disease
* BP6 Reputable source recently reports variant as benign, but the evidence is not available to the laboratory to perform an independent evaluation
* BP7 A synonymous (silent) variant for which splicing prediction algorithms predict no impact to the splice consensus sequence nor the creation of a new splice site AND the nucleotide is not highly conserved
'''

import os
import json
import pandas as pd
from picus import data
data_path = data.__path__[0]

hgvsp = 'HGVSp'
gene_symbol = 'SYMBOL'
transcript_consequence_terms = 'Consequence'
ALT = 'ALT'
gnomad = 'gnomAD_AF'
polyphen = 'PolyPhen'
sift = 'SIFT'
af = 'AF'


class EvidenceCollection:

    def __init__(self):
        self.evidences = ['PVS1', 'PS1', 'PS2', 'PS3', 'PS4', 'PM1', 'PM2', 'PM3', 'PM4', 'PM5', 'PM6', 'PP1', 'PP2', 'PP3', 'PP4', 'PP5', 'BA1', 'BS1', 'BS2', 'BS3', 'BS4', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'BP6', 'BP7']
        lof_genes = pd.read_csv(
            os.path.join(data_path, 'lof_genes.tsv'),
            sep='\t'
        )
        self.lof_genes = lof_genes['gene_symbol'].tolist()

        null_variants = pd.read_csv(
            os.path.join(data_path, 'variant_consequences.tsv'),
            sep='\t'
        )
        self.null_variants = null_variants[null_variants['IMPACT'] == 'HIGH']['SO term'].tolist()

        # PS4 from InterVar (Change it later)
        ps4_ids = pd.read_csv(
            os.path.join(data_path, 'PS4.tsv'),
            sep='\t'
        )
        self.ps4_ids = ps4_ids['id'].tolist()
        # PP2 Gene list from InterVar
        pp2_genes = pd.read_csv(
            os.path.join(data_path, 'PP2.tsv'),
            sep='\t'
        )
        self.pp2_genes = pp2_genes['gene_symbol'].tolist()

        bp1_genes = pd.read_csv(
            os.path.join(data_path, 'BP1.tsv'),
            sep='\t'
        )
        self.bp1_genes = bp1_genes['gene_symbol'].tolist()

    def collect_evidences(self, df):
        # merge to check for PS1
        df.POS = df.POS.astype(int)

        # To Do (evidences to collect)
        df['PVS1'] = df.apply(self.get_PVS1, axis=1)
        df['PS1'] = df.apply(self.get_PS1, axis=1)
        df['PS2'] = df.apply(self.get_PS2, axis=1)
        df['PS3'] = df.apply(self.get_PS3, axis=1)
        df['PS4'] = df.apply(self.get_PS4, axis=1)
        df['PM1'] = df.apply(self.get_PM1, axis=1)
        df['PM2'] = df.apply(self.get_PM2, axis=1)
        df['PM3'] = df.apply(self.get_PM3, axis=1)
        df['PM4'] = df.apply(self.get_PM4, axis=1)
        df['PM5'] = df.apply(self.get_PM5, axis=1)
        df['PM6'] = df.apply(self.get_PM6, axis=1)
        df['PP1'] = df.apply(self.get_PP1, axis=1)
        df['PP2'] = df.apply(self.get_PP2, axis=1)
        df['PP3'] = df.apply(self.get_PP3, axis=1)
        df['PP4'] = df.apply(self.get_PP4, axis=1)
        df['PP5'] = df.apply(self.get_PP5, axis=1)
        df['BA1'] = df.apply(self.get_BA1, axis=1)
        df['BS1'] = df.apply(self.get_BS1, axis=1)
        df['BS2'] = df.apply(self.get_BS2, axis=1)
        df['BS3'] = df.apply(self.get_BS3, axis=1)
        df['BS4'] = df.apply(self.get_BS4, axis=1)
        df['BP1'] = df.apply(self.get_BP1, axis=1)
        df['BP2'] = df.apply(self.get_BP2, axis=1)
        df['BP3'] = df.apply(self.get_BP3, axis=1)
        df['BP4'] = df.apply(self.get_BP4, axis=1)
        df['BP5'] = df.apply(self.get_BP5, axis=1)
        df['BP6'] = df.apply(self.get_BP6, axis=1)
        df['BP7'] = df.apply(self.get_BP7, axis=1)

        df['evidences'] = '{' + \
            '"PVS1": ' + df['PVS1'] + \
            ', "PS1": ' + df['PS1'] + \
            ', "PS2": ' + df['PS2'] + \
            ', "PS3": ' + df['PS3'] + \
            ', "PS4": ' + df['PS4'] + \
            ', "PM1": ' + df['PM1'] + \
            ', "PM2": ' + df['PM2'] + \
            ', "PM3": ' + df['PM3'] + \
            ', "PM4": ' + df['PM4'] + \
            ', "PM5": ' + df['PM5'] + \
            ', "PM6": ' + df['PM6'] + \
            ', "PP1": ' + df['PP1'] + \
            ', "PP2": ' + df['PP2'] + \
            ', "PP3": ' + df['PP3'] + \
            ', "PP4": ' + df['PP4'] + \
            ', "PP5": ' + df['PP5'] + \
            ', "BA1": ' + df['BA1'] + \
            ', "BS1": ' + df['BS1'] + \
            ', "BS2": ' + df['BS2'] + \
            ', "BS3": ' + df['BS3'] + \
            ', "BS4": ' + df['BS4'] + \
            ', "BP1": ' + df['BP1'] + \
            ', "BP2": ' + df['BP2'] + \
            ', "BP3": ' + df['BP3'] + \
            ', "BP4": ' + df['BP4'] + \
            ', "BP5": ' + df['BP5'] + \
            ', "BP6": ' + df['BP6'] + \
            ', "BP7": ' + df['BP7'] + \
            '}'

        df.drop(self.evidences, axis=1, inplace=True)

        return df

    def flat_evidences(self, evidences):
        evidences_dict = json.loads(evidences)
        evidence_str = ''
        for evidence in self.evidences:
            if evidences_dict[evidence] == 1:
                evidence_str += '{} '.format(evidence)
        return evidence_str

    # Pathogenic

    # Pathogenic Very Strong
    def get_PVS1(self, df):
        if df[gene_symbol] in self.lof_genes and df[transcript_consequence_terms] in self.null_variants:
            return '1'
        else:
            return '0'

    # Pathogenic Strong
    def get_PS1(self, df):
        return '0'

    def get_PS2(self, df):
        return '0'

    def get_PS3(self, df):
        return '0'

    def get_PS4(self, df):
        return '0'
        # if df['id'] in self.ps4_ids:
        #     return '1'
        # else:
        #     return '0'

    # Pathogenic Moderate
    def get_PM1(self, df):
        return '0'

    def get_PM2(self, df):
        if df[gnomad] < .001:
            return '1'
        else:
            return '0'

    def get_PM3(self, df):
        return '0'

    def get_PM4(self, df):
        if df[transcript_consequence_terms] in ["inframe_insertion", "inframe_deletion", "stop_lost"]:
            return '1'
        else:
            return '0'

    def get_PM5(self, df):
        return '0'

    def get_PM6(self, df):
        return '0'

    # Pathogenic Supporting
    def get_PP1(self, df):
        return '0'

    def get_PP2(self, df):
        if df[gene_symbol] in self.pp2_genes and df[transcript_consequence_terms] == 'missense_variant':
            return '1'
        else:
            return '0'

    def get_PP3(self, df):
        '''
        cutoffs from
        https://www.ensembl.org/info/genome/variation/prediction/protein_function.html
        '''
        try:
            if float(df[sift].split('(')[1].split(')')[0]) < 0.05 and float(df[polyphen].split('(')[1].split(')')[0]) > 0.908:
                return '1'
            else:
                return '0'
        except:
            return '0'

    def get_PP4(self, df):
        return '0'

    def get_PP5(self, df):
        if df['ClinVar_CLNSIG'] == 'Pathogenic':
            return '1'
        else:
            return '0'

    # Benign

    # Benign Stand-alone
    def get_BA1(self, df):
        if df[af] > 0.05 or df[gnomad] > 0.05:
            return '1'
        else:
            return '0'

    # Benign Strong
    def get_BS1(self, df):
        return '0'

    def get_BS2(self, df):
        return '0'

    def get_BS3(self, df):
        return '0'

    def get_BS4(self, df):
        return '0'

    # Benign Supporting
    def get_BP1(self, df):
        if df[gene_symbol] in self.bp1_genes and df[transcript_consequence_terms] == 'missense_variant':
            return '1'
        else:
            return '0'

    def get_BP2(self, df):
        return '0'

    def get_BP3(self, df):
        return '0'

    def get_BP4(self, df):
        '''
        cutoffs from
        https://www.ensembl.org/info/genome/variation/prediction/protein_function.html
        '''
        try:
            if float(df[sift].split('(')[1].split(')')[0]) >= 0.05 and float(df[polyphen].split('(')[1].split(')')[0]) <= 0.446:
                return '1'
            else:
                return '0'
        except:
            return '0'

    def get_BP5(self, df):
        return '0'

    def get_BP6(self, df):
        if df['ClinVar_CLNSIG'] == 'Benign':
            return '1'
        else:
            return '0'

    def get_BP7(self, df):
        return '0'
