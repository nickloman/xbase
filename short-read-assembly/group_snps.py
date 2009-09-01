import sys

hash = {}

args = sys.argv[1:]
for arg in args:
	fh = open(arg)
	for ln in fh:
		ln = ln.rstrip()
		cols = ln.split("\t")
		hash_arg = "%s-%s" % (cols[0], cols[1])
		if hash_arg in hash:
			hash[hash_arg].append(ln)
		else:
			hash[hash_arg] = [ln]

keys = hash.keys()
keys.sort()
for key in keys:
	val = hash[key]
	if len(val) == len(args):
		i = 1
		for ln in val:
			print "%d: %s" % (i, ln)
			i += 1
