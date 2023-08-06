from contig_tools.file_parsing import import_contig_records
import json

def Nx(contig_lengths, x = 50):
    '''return Nx of a list of contig lengths'''
    contig_lengths.sort(reverse=1)
    Nx_threshold = sum(contig_lengths) * x / 100
    
    cumulative_length = 0
    for length in contig_lengths:
        cumulative_length += length
        if cumulative_length >= Nx_threshold:
            Nx = length
            return Nx

def get_contig_metrics(contigs):
    '''return a dictionary of contig metrics given a list of BioPython Seq objects'''
    contig_metrics = {}
    # make a list of contig lengths
    contig_lengths = [len(contig.seq) for contig in contigs]
    number_of_gcs = sum([sum(map(contig.seq.upper().count, ['G', 'C'])) for contig in contigs])
    contig_metrics['Number of contigs'] = len(contig_lengths)
    contig_metrics['Number of contigs > 500bp'] = len([filtered_length for filtered_length in contig_lengths if filtered_length > 500])
    contig_metrics['Total length'] = sum(contig_lengths)
    contig_metrics['%GC'] = number_of_gcs/sum(contig_lengths)*float(100)
    contig_metrics['Largest contig'] = max(contig_lengths)
    contig_metrics['N{0} score'.format(50)] = Nx(contig_lengths, x = 50)
    return contig_metrics

def print_contig_metrics(fasta_file_path, format='tsv'):
    '''Print out contig metrics given the path to a fasta file containing multiple contigs'''
    contigs = import_contig_records(fasta_file_path)
    contig_metrics = get_contig_metrics(contigs)
    if format == 'tsv':
        print('metric\tvalue')
        for metric in sorted(contig_metrics.keys()):
                print('{0}\t{1}'.format(metric, contig_metrics[metric]))
    elif format == 'json':
        print(json.dumps(contig_metrics, indent=2))

