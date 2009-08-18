import os

from types import ListType

def add_qualifier(feature, key, value):
	if not isinstance(value, ListType):
		value = [value]
	if key in feature.qualifiers:
		feature.qualifiers[key].extend(value)
	else:
		feature.qualifiers[key] = value

def get_prefix(path):
	head, tail = os.path.split(path)
	prefix, suffix = os.path.splitext(tail)
	return prefix

