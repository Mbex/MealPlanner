#!/home/mikbok/anaconda/bin/python

import re

def discern_type(item):
    """Return correct type for item - either int, str, or tupe of int and str."""
    try:
        item = int(item)
    except:
        valandunit = re.match(r"([0-9]+)([a-z]+)", item, re.I)
        if valandunit:
            item = valandunit.groups()
    return item


def consolidate_list(items):
    """Consolidates multiple items based on type."""
    ints = 0
    strings = {}
    mixed = {}
    for item in items:
        print item
        if isinstance(item, int):
            ints += item
        if isinstance(item, str):
            try:
                strings[item] = string[item] + 1
            except:
                strings[item] = 1
        if isinstance(item, tuple):
            amount = int(item[0])
            unit = item[1]
            try:
                mixed[unit] = mixed[unit] + amount
            except:
                mixed[unit] = amount
    return ints, strings, mixed
