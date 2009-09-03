#!/usr/bin/python

import sys

i = sys.stdin.__iter__()
header = i.next()
header_cols = header.rstrip().split('\t')
print "<table>"
print "<tr>"
for x in header_cols:
    print " <th>%s</th>" % (x)
print "</tr>"

while 1:
    try:
        ln = i.next()
        print "<tr>"
        cols = ln.rstrip().split('\t')
        for x in cols:
            print " <td>%s</td>" % (x.strip())
        print "</tr>"
    except StopIteration:
        break
    
print "</table>"
