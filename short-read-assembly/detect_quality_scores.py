import sys

total_max = None
total_min = None
fh = open(sys.argv[1])
iter = fh.__iter__()
while 1:
	iter.next()
	iter.next()
	iter.next()
	quals = iter.next()
	print quals

	a = min([ord(x) for x in quals.rstrip()])
	b = max([ord(x) for x in quals.rstrip()])

	if total_min == None or a < total_min:
		total_min = a
	if total_max == None or b > total_max:
		total_max = b

	print "%d %d" % (total_min, total_max)


	

