# coding: utf-8

'''
# Classification

### Pathogenic

#### (i) 1 Very strong (PVS1) AND
* (a) ≥1 Strong (PS1–PS4) OR
* (b) ≥2 Moderate (PM1–PM6) OR
* (c) 1 Moderate (PM1–PM6) and 1 supporting (PP1–PP5) OR
* (d) ≥2 Supporting (PP1–PP5)

#### (ii) ≥2 Strong (PS1–PS4) OR

#### (iii) 1 Strong (PS1–PS4) AND
* (a)≥3 Moderate (PM1–PM6) OR
* (b)2 Moderate (PM1–PM6) AND ≥2 Supporting (PP1–PP5) OR
* (c)1 Moderate (PM1–PM6) AND ≥4 supporting (PP1–PP5)

### Likely pathogenic

#### (i)  1 Very strong (PVS1) AND 1 moderate (PM1–PM6) OR

#### (ii)  1 Strong (PS1–PS4) AND 1–2 moderate (PM1–PM6) OR

#### (iii)  1 Strong (PS1–PS4) AND ≥2 supporting (PP1–PP5) OR

#### (iv)  ≥3 Moderate (PM1–PM6) OR

#### (v)  2 Moderate (PM1–PM6) AND ≥2 supporting (PP1–PP5) OR

#### (vi)  1 Moderate (PM1–PM6) AND ≥4 supporting (PP1–PP5)

### Benign

#### (i) 1 Stand-alone (BA1) OR

#### (ii) ≥2 Strong (BS1–BS4)

### Likely benign

#### (i)  1 Strong (BS1–BS4) and 1 supporting (BP1–BP7) OR

#### (ii) ≥2 Supporting (BP1–BP7)

### Uncertain significance

#### (i) Other criteria shown above are not met OR

#### (ii)  the criteria for benign and  pathogenic are contradictory
'''

import json


class VariantClassification:

    def __init__(self):
        pass

    def classify_variant(self, evidences, single_out):
        self.evidences = json.loads(evidences)
        self.variant_significance = {'pathogenic': 0,
                                     'likely_pathogenic': 0,
                                     'benign': 0,
                                     'likely_benign': 0,
                                     'uncertain_significance': 0}

        # Check pathogenic
        if self.is_pathogenic():
            self.variant_significance['pathogenic'] = 1
        # Check likely_pathogenic if pathogenic is False
        elif self.is_likely_pathogenic():
            self.variant_significance['likely_pathogenic'] = 1

        # Check benign
        if self.is_benign():
            self.variant_significance['benign'] = 1
        # Check likely_benign if benign is False
        elif self.is_likely_benign():
            self.variant_significance['likely_benign'] = 1

        # check uncertain significance
        # (i) Other criteria shown above are not met OR
        if sum(self.variant_significance.values()) == 0:
            self.variant_significance['uncertain_significance'] = 1
        # (ii)  the criteria for benign and  pathogenic are contradictory
        elif self.variant_significance['pathogenic'] == 1 and self.variant_significance['benign'] == 1:
            self.variant_significance['uncertain_significance'] = 1
            self.variant_significance['pathogenic'] = 0
            self.variant_significance['benign'] = 0

        if single_out:
            if sum(self.variant_significance.values()) == 1:
                for k, v in self.variant_significance.items():
                    if v == 1:
                        return k
            else:
                return 'unknown'
        else:
            return self.variant_significance

    def get_evidence_group(self, group):
        return [self.evidences[evidence] for evidence in self.evidences if group in evidence]

    def is_pathogenic(self):
        # (i) 1 Very strong (PVS1) AND
        if self.evidences['PVS1'] == 1 and (
            # (a) ≥1 Strong (PS1–PS4) OR
            sum(self.get_evidence_group('PS')) >= 1 or
            # (b) ≥2 Moderate (PM1–PM6) OR
            sum(self.get_evidence_group('PM')) >= 2 or (
                # (c) 1 Moderate (PM1–PM6) and 1 supporting (PP1–PP5) OR
                sum(self.get_evidence_group('PM')) >= 1 and
                sum(self.get_evidence_group('PP')) >= 1) or
            # (d) ≥2 Supporting (PP1–PP5)
                sum(self.get_evidence_group('PP')) >= 2):
            return True

        # (ii) ≥2 Strong (PS1–PS4) OR
        elif sum(self.get_evidence_group('PS')) >= 2:
            return True

        # (iii) 1 Strong (PS1–PS4) AND
        elif sum(self.get_evidence_group('PS')) >= 1 and (
            # (a) ≥3 Moderate (PM1–PM6) OR
            sum(self.get_evidence_group('PM')) >= 3 or (
                # (b) 2 Moderate (PM1–PM6) AND ≥2 Supporting (PP1–PP5) OR
                sum(self.get_evidence_group('PM')) >= 2 and
                sum(self.get_evidence_group('PP')) >= 2) or (
                # (c) 1 Moderate (PM1–PM6) AND ≥4 supporting (PP1–PP5)
                sum(self.get_evidence_group('PM')) >= 1 and
                sum(self.get_evidence_group('PP')) >= 4)):
            return True
        else:
            return False

    def is_likely_pathogenic(self):
        # (i) 1 Very strong (PVS1) AND 1 moderate (PM1–PM6) OR
        if self.evidences['PVS1'] == 1 and sum(self.get_evidence_group('PM')) >= 1:
            return True

        # (ii) 1 Strong (PS1–PS4) AND 1–2 moderate (PM1–PM6) OR
        elif sum(self.get_evidence_group('PS')) >= 1 and sum(self.get_evidence_group('PM')) >= 1:
            return True

        # (iii) 1 Strong (PS1–PS4) AND ≥2 supporting (PP1–PP5) OR
        elif sum(self.get_evidence_group('PS')) >= 1 and sum(self.get_evidence_group('PP')) >= 2:
            return True

        # (iv) ≥3 Moderate (PM1–PM6) OR
        elif sum(self.get_evidence_group('PM')) >= 3:
            return True
        # (v) 2 Moderate (PM1–PM6) AND ≥2 supporting (PP1–PP5) OR
        elif sum(self.get_evidence_group('PM')) >= 2 and sum(self.get_evidence_group('PP')) >= 2:
            return True

        # (vi) 1 Moderate (PM1–PM6) AND ≥4 supporting (PP1–PP5)
        elif sum(self.get_evidence_group('PM')) >= 1 and sum(self.get_evidence_group('PP')) >= 4:
            return True
        else:
            return False

    def is_benign(self):
        # (i) 1 Stand-alone (BA1) OR
        if self.evidences['BA1'] == 1:
            return True
        # (ii) ≥2 Strong (BS1–BS4)
        elif sum(self.get_evidence_group('BS')) >= 2:
            return True
        else:
            return False

    def is_likely_benign(self):
        # (i)  1 Strong (BS1–BS4) and 1 supporting (BP1–BP7) OR
        if sum(self.get_evidence_group('PS')) >= 1 and sum(self.get_evidence_group('BP')) >= 1:
            return True
        # (ii) ≥2 Supporting (BP1–BP7)
        elif sum(self.get_evidence_group('BP')) >= 2:
            return True
        else:
            return False
