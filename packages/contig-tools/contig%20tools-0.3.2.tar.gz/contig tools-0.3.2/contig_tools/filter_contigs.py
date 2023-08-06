import sys, re
from Bio import SeqIO
from contig_tools.file_parsing import import_contig_records 
from contig_tools.utility import get_logger

cov_pattern = re.compile("cov_([0-9.]+)")
logger = get_logger(__file__)

def filtered_contigs_generator(contigs, min_length = 500, min_coverage = None):
    total_contigs = 0
    contigs_kept = 0
    for contig in contigs:
        total_contigs = total_contigs + 1
        result = cov_pattern.search(contig.name)
        if not min_coverage and len(contig) >= min_length:
            contigs_kept = contigs_kept + 1
            yield contig
        elif result and float(result.group(1)) >= min_coverage and len(contig) >= min_length:
            contigs_kept = contigs_kept + 1
            yield contig
        elif len(contig) >= min_length:
            logger.warn('No coverage encoded in contig name')
            contigs_kept = contigs_kept + 1
            yield contig

    print("Starting contigs: {0}\nContigs kept: {1}".format(total_contigs, contigs_kept))

def filter_contig_file(fasta_file_path, min_contig_length, min_contig_coverage, output_file = None):
    if not output_file:
        output_file = fasta_file_path.replace('fa', 'filter_gt_{0}bp_gt_{1}cov.fa'.format(min_contig_length, min_contig_coverage))
    contigs = import_contig_records(fasta_file_path)
    with open(output_file, 'w') as filtered_fasta:
            SeqIO.write(filtered_contigs_generator(contigs,
                min_length = min_contig_length,
                min_coverage = min_contig_coverage),
                filtered_fasta, 'fasta')
