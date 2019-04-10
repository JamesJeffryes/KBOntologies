import sys
import time
import json
from collections import defaultdict


def parse_divisions(path):
    return {str(i): x.split('\t')[4] for i, x in enumerate(open(path))}


def parse_names(path):
    aliases = defaultdict(list)
    for line in open(path):
        sl = line.split('\t')
        aliases[sl[0]].append(sl[2])
    return aliases


def parse_lineages(path):
    names, lineages = {}, {}
    for line in open(path):
        sl = line.split('\t')
        names[sl[0]] = sl[2]
        lineages[sl[0]] = sl[4]
    return names,lineages


if __name__ == "__main__":
    taxa = {}
    _, dump_path, out_path = sys.argv
    divisions = parse_divisions(f'{dump_path}/division.dmp')
    aliases = parse_names(f'{dump_path}/names.dmp')
    scientific_names, lineages = parse_lineages(f'{dump_path}/fullnamelineage.dmp')
    for line in open(f'{dump_path}/nodes.dmp'):
        sl = line.split('\t')
        taxa[f'NCBI:txid{sl[0]}'] = {
            'id': f'NCBI:txid{sl[0]}',
            'is_a': [f'NCBI:txid{sl[2]} ! {scientific_names[sl[2]]}'],
            'synonym': aliases[sl[0]],
            'name': scientific_names[sl[0]],
            'def': [f'Genetic Code:{sl[12]}',
                    f'Rank:{sl[4]}',
                    f'Division:{divisions[sl[8]]}',
                    f'Lineage:{lineages[sl[0]]}',
                    ],
        }
    current_time = time.localtime()
    ontology_dict = {
        'ontology': "NCBI Taxonomy",
        'date': time.strftime('%m:%d:%Y %H:%M', current_time),
        "format_version": "N/A",
        'term_hash': taxa,
    }
    json.dump(ontology_dict, open(out_path, 'w'))




