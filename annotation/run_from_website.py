
import pickle
import sys
import os
import settings

['species_name', 'nucleotide_file', 'reference_strain', 'strain_identifier', 'gene_min_length', 'training_model', 'gene_max_overlap', 'blast_evalue_cutoff', 'email_address', 'reference_file']

class CommandRunner:
    def __init__(self, base_dir, commands):
        self.base_dir = base_dir
        self.commands = commands

    def run(self, command_name, *args, **kwargs):
        # TODO make this use subprocess module not shell

        command_entry = self.commands[command_name]
        arg_list = []
        for arg in command_entry['args']:
            arg_list.append(kwargs[arg])
        arg_list = tuple(arg_list)
        full_command = command_entry['cmd'] % arg_list
        in_file = kwargs.get('in_file', None)
        if in_file:
            full_command += " < %s/%s" % (self.base_dir, in_file)
        out_file = kwargs.get('out_file', None)
        if out_file:
            full_command += " > %s/%s" % (self.base_dir, out_file)
        print full_command
        os.system(full_command)

COMMANDS = {
    'run-glimmer' : {
        'cmd' : 'python run_glimmer.py "%s" "%s" "%s" "%s" "%s" "%s"',
        'args' : ['working_dir', 'ref', 'seq', 'gene_min_length', 'gene_max_overlap', 'training_model']
    },
    'glimmer-to-genbank' : {
        'cmd' : 'python glimmer_to_genbank.py "%s" "%s"',
        'args' : ['seq', 'predict_file']
    },
    'relabel-cds' : {
        'cmd' : 'python relabel_cds.py "%s_"',
        'args' : ['prefix']
    },
    'add-translations-to-genbank' : {
        'cmd' : 'python add_translations_to_genbank.py',
        'args' : []
    },
    'dump-translations-to-fasta' : {
        'cmd' : 'python dump_translations_to_fasta.py',
        'args' : []
    },
    'formatdb' : {
        'cmd' : '%s/formatdb -p T -i %s',
        'args' : ['blast_bin_path', 'database']
    },
    'blast' : {
        'cmd' : '%s/blastall -p blastp -d "%s" -i "%s" -m 7 -a 4 -v 10 -b 10 -F T',
        'args' : ['blast_bin_path', 'database', 'query']
    },
    'add-blast-results-to-genbank' : {
        'cmd' : 'python add_blast_results_to_genbank.py "%s" "%s" "%s"',
        'args' : ['seq', 'blast_file', 'threshold']
    },
}

base_dir = sys.argv[1]
param_file = "%s/params.obj" % (base_dir)
with open(param_file) as fh:
    params = pickle.load(fh)

reference_file = "%s/ref.fna" % (base_dir)
starter_file = "%s/seq.fna" % (base_dir)

runner = CommandRunner(base_dir, COMMANDS)
runner.run('run-glimmer',
    working_dir=base_dir,
    ref=reference_file,
    seq=starter_file,
    gene_min_length=params['gene_min_length'],
    gene_max_overlap=params['gene_max_overlap'],
    training_model=params['training_model']
)
runner.run('glimmer-to-genbank',
    out_file='seq.gb1',
    seq=starter_file,
    predict_file="%s/seq.predict" % (base_dir)
)
runner.run('relabel-cds',
    in_file='seq.gb1',
    out_file='seq.gb2',
    prefix=params['strain_identifier']
)
runner.run('add-translations-to-genbank',
    in_file='seq.gb2',
    out_file='seq.gb3'
)
runner.run('dump-translations-to-fasta',
    in_file='seq.gb3',
    out_file='seq.protein.faa'
)
runner.run('formatdb',
    blast_bin_path = settings.BLAST_DIRECTORY + '/bin',
    database="%s/ref.faa" % (base_dir)
)
runner.run('blast',
    blast_bin_path = settings.BLAST_DIRECTORY + '/bin',
    database="%s/ref.faa" % (base_dir),
    query="%s/seq.protein.faa" % (base_dir),
    out_file='blast_results.xml'
)
runner.run('add-blast-results-to-genbank',
    seq="%s/seq.gb3" % (base_dir),
    blast_file="%s/blast_results.xml" % (base_dir),
    threshold=params['blast_evalue_cutoff'],
    out_file='seq.gb4',
)
 
