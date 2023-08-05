import urllib.request
from picus import data_path


def download_clinvar():
    urllib.request.urlretrieve('https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz', data_path.joinpath('clinvar.vcf.gz'))
    urllib.request.urlretrieve('https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/clinvar.vcf.gz.tbi', data_path.joinpath('clinvar.vcf.gz.tbi'))
