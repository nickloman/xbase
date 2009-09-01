#!/usr/bin/python

from django.core.mail import send_mail
import pickle
import sys
import os
import settings

success_message = """
The automated annotation for %s %s you recently requested has completed.

You may access the result files at:

%s/%s/

Regards,

xBASE Annotation Service

"""

['species_name', 'nucleotide_file', 'reference_strain', 'strain_identifier', 'gene_min_length', 'training_model', 'gene_max_overlap', 'blast_evalue_cutoff', 'email_address', 'reference_file']

class CommandRunner:
    def __init__(self, base_dir, commands):
        self.base_dir = base_dir
        self.commands = commands
        self.log = open(self.base_dir + '/log.txt', 'w')

    def run(self, command_name, *args, **kwargs):
        # TODO make this use subprocess module not shell

        command_entry = self.commands[command_name]
        arg_list = []
        for arg in command_entry['args']:
            arg_list.append(kwargs[arg])
        arg_list = tuple(arg_list)
        full_command = command_entry['cmd'] % arg_list
        if not full_command.startswith('/'):
            full_command = script_dir + '/' + full_command
        in_file = kwargs.get('in_file', None)
        if in_file:
            full_command += " < %s/%s" % (self.base_dir, in_file)
        out_file = kwargs.get('out_file', None)
        if out_file:
            full_command += " > %s/%s" % (self.base_dir, out_file)
        print full_command
        print >>self.log, full_command
        self.log.flush()

        if os.system(full_command):
            print "%s execution failed" % (full_command)
            raise SystemExit

COMMANDS = {
    'run-glimmer' : {
        'cmd' : 'run_glimmer.py "%s" "%s" "%s" "%s" "%s" "%s"',
        'args' : ['working_dir', 'ref', 'seq', 'gene_min_length', 'gene_max_overlap', 'training_model']
    },
    'glimmer-to-genbank' : {
        'cmd' : 'glimmer_to_genbank.py "%s" "%s"',
        'args' : ['seq', 'predict_file']
    },
    'relabel-cds' : {
        'cmd' : 'relabel_cds.py "%s_"',
        'args' : ['prefix']
    },
    'add-translations-to-genbank' : {
        'cmd' : 'add_translations_to_genbank.py',
        'args' : []
    },
    'remove-overlaps-with-frameshifts' : {
        'cmd' : 'remove_overlaps_with_frameshifts.py',
        'args' : []
    },
    'dump-translations-to-fasta' : {
        'cmd' : 'dump_translations_to_fasta.py',
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
        'cmd' : 'add_blast_results_to_genbank.py "%s" "%s" "%s"',
        'args' : ['seq', 'blast_file', 'threshold']
    },
    'annotate-by-seqfeature' : {
        'cmd' : 'annotate_by_seqfeature.py "%s"',
        'args' : ['seq'],
    },
    'make-art-file' : {
        'cmd' : 'make-art-file.py "%s"',
        'args' : ['prefix'],
    },
}

try:
    base_dir = sys.argv[1]
except IndexError:
    print "Usage: %s <annotation directory>" % (sys.argv[0])

script_dir, script_name = os.path.split(sys.argv[0])

param_file = "%s/params.obj" % (base_dir)
with open(param_file) as fh:
    params = pickle.load(fh)

reference_file = "%s/ref.fna" % (base_dir)
starter_file = "%s/seq.fna" % (base_dir)

runner = CommandRunner(base_dir, COMMANDS)
runner.run('run-glimmer',
    script_dir=script_dir,
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
runner.run('remove-overlaps-with-frameshifts',
    in_file='seq.gb3',
    out_file='seq.gb4',
)
runner.run('dump-translations-to-fasta',
    in_file='seq.gb4',
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
    seq="%s/seq.gb4" % (base_dir),
    blast_file="%s/blast_results.xml" % (base_dir),
    threshold=params['blast_evalue_cutoff'],
    out_file='seq.gb5',
)
runner.run('annotate-by-seqfeature',
    seq="%s/seq.gb5" % (base_dir),
    out_file='seq.gbk',
)
runner.run('make-art-file',
    in_file="%s/seq.gbk" % (base_dir),
    out_file="%s/seq_concat.gbk" % (base_dir),
    prefix=params['strain_identifier']
)

html_report = open("%s/index.html" % (base_dir), "w")
print >>html_report, """
<html>
    <head>
        <title>xBASE Annotation for %s %s</title>
    </head>
    <body>
        <h1>%s %s annotation</h1>
        <h2>Sequence Files</h2>
        <p>
            <ul>
                <li><a href="seq.gbk">Annotation in GenBank format</a>
                <li><a href="seq_concat.gbk">Concatenated annotation in GenBank format (good for Artemis/ACT)</a>
                <li><a href="seq.fna">Original sequence in FASTA format</a>
                <li><a href="seq.protein.faa">Predicted protein sequences in FASTA format</a>
            </ul>
        </p>
        <h2>%s (Reference)</h2>
        <p>
            <ul>
                <li><a href="ref.fna>"Reference sequence in FASTA format</a>
            </ul>
        </p>
        <h2>Miscellanous Files</h2>
        <p>
            <ul>
                <li><a href="log.txt">Log file of commands</a>
            </ul>
        </p>
        <hr>
        <a href="mailto:n.j.loman@bham.ac.uk">n.j.loman@bham.ac.uk</a>
    </body>
</html>
""" % (params['species_name'],
    params['strain_identifier'],
    params['species_name'],
    params['strain_identifier'],
    params['reference_strain'])
html_report.close()

send_mail("Your xBASE Genome Annotation %s" % (params['reference_number']),
    success_message % (params['species_name'],
        params['strain_identifier'],
        settings.ANNOTATION_HTROOT, 
        params['results_directory_identifier'],
        base_dir),
    'n.j.loman@bham.ac.uk',
    [params['email_address']],
    fail_silently=False)

