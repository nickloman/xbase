import sys

n = 0
lines = 0
for ln in sys.stdin.readlines():
    n += float(ln.rstrip())
    lines += 1

print "%s" % (float(n) / lines)

