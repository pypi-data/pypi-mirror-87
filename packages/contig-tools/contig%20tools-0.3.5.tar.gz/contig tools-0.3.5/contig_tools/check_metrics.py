from contig_tools.file_parsing import import_contig_records
from contig_tools.contig_metrics import get_contig_metrics
from contig_tools.utility import get_logger

import yaml

logger = get_logger(__file__)

def print_check_contig_metrics(fasta_file_path, conditions_yml_file):
    '''Print results of checking contig metrics'''
    contigs = import_contig_records(fasta_file_path)
    contig_metrics = get_contig_metrics(contigs)
    result, failure_reasons = check_contig_metrics(contig_metrics, conditions_yml_file)

    print(result)
    if not result:
        for reason in failure_reasons:
            print(reason)

def check_contig_metrics(contig_metrics, conditions_yml_file):
    '''Check metrics of contigs based on conditions defined in a yaml file '''


    # check each condition
    failure_reasons = []
    all_pass = True
    with open(conditions_yml_file) as conditions_yml:
        conditions = yaml.load(conditions_yml)
        for metric_name in conditions:
            try:
                metric_value = contig_metrics[metric_name]
                condition_value = conditions[metric_name]['condition_value']
                # possible conditions
                # greater than
                if conditions[metric_name]['condition_type'] == 'gt':
                    if not metric_value > condition_value:
                        all_pass = False
                        failure_reasons.append('{0}: {1} not > {2}'.format(metric_name, metric_value, condition_value))
                # less than
                elif conditions[metric_name]['condition_type'] == 'lt':
                    if not metric_value < condition_value:
                        all_pass = False
                        failure_reasons.append('{0}: {1} not < {2}'.format(metric_name, metric_value, condition_value))
                # less than and greater than
                elif conditions[metric_name]['condition_type'] == 'lt_gt':
                    if not (metric_value < condition_value[0] and metric_value > condition_value[1]):
                        all_pass = False
                        failure_reasons.append('{0}: not {1} > {2} > {3}'.format(metric_name,condition_value[0], metric_value, condition_value[1]))

            except KeyError as e:
                logger.error("No such key {0}. The available metrics are {1}".format(e, ", ".join(contig_metrics.keys())))

        if all_pass:
            return True, []
        else:
           return False, failure_reasons
    
