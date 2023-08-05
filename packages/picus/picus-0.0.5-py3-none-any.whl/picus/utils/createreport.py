from subprocess import Popen
import json
import os
from os.path import basename, splitext
from picus import templates


class CreateReport:

    def __init__(self, variants, template, report_data, command, group, output_file, keep=False):
        self.variants = variants
        self.command = command
        self.template = template
        with open(report_data) as f:
            self.report_data = json.load(f)
        self.group = group
        self.output_file = output_file
        self.keep = keep

        if self.report_data['header']['logo'] == 'default':
            self.report_data['header']['logo'] = os.path.join(
                templates.__path__[0], 'picus.png')

    def group_variants(self, groups):
        return {group: [variant for variant in self.variants if group in variant['significance']] for group in groups}

    def create_report(self):
        self.grouped_variants = self.group_variants(
            ['pathogenic', 'benign', 'uncertain'])
        self.report_data['variants'] = self.grouped_variants

        report_json = '{}.json'.format(
            splitext(basename(self.output_file))[0]
        )
        with open(report_json, 'w') as f:
            json.dump(self.report_data, f)

        with open(self.template) as f:
            template_str = f.read()
        template_str = template_str.replace('report_data.json', report_json)
        report_rnw = '{}.Rnw'.format(
            splitext(basename(self.output_file))[0]
        )
        with open(report_rnw, 'w') as f:
            f.write(template_str)

        report_tex = '{}.tex'.format(
            splitext(basename(self.output_file))[0]
        )

        cmd = 'R -e "library(knitr);knit(\'{}\', output=\'{}\')"'.format(
            report_rnw, report_tex)
        p = Popen(cmd, shell=True)
        output, error = p.communicate()

        p = Popen('pdflatex {}'.format(report_tex), shell=True)
        output, error = p.communicate()

        if not self.keep:
            os.remove(report_rnw)
            os.remove(report_json)
            os.remove(report_tex)
