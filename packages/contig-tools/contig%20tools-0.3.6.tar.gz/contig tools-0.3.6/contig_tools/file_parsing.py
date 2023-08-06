from Bio import SeqIO
def import_contig_records(fasta_file_path):
    '''Make a list of Seq records from a fasta filepath''' 
    contigs = []
    for record in SeqIO.parse(fasta_file_path, 'fasta'):
        contigs.append(record)
    return contigs