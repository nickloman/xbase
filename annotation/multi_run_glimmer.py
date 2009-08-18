import os, sys
import utils

GLIMMER_PATH = "../../pkg/glimmer3.02/bin/"
GLIMMER_ARGS = "-o 50 -g110 -t30"

for file in os.listdir(sys.argv[1]):
	if not file.endswith('.fna'):
		continue
	print file

	prefix = utils.get_prefix(file)

	cmd = "%s/glimmer3 %s %s/%s %s %s" % (GLIMMER_PATH, GLIMMER_ARGS, sys.argv[1], file, sys.argv[2], prefix)
	print cmd
	os.system(cmd)


