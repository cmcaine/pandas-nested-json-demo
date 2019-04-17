import json

import collections
import itertools

import pandas as pd

def flatten2d(it):
    return list(itertools.chain(*it))


def frequencies(it):
    counter = collections.Counter(it)
    return collections.OrderedDict(sorted(counter.items()))


with open("data/mock-drug-groups.json") as f:
    drugjson = json.load(f)

# drugjson is a list containing one dictionary for each drug group
# drug groups have an id, name and list of drugs (which have a name, id and list of "testables"
[d.keys() for d in drugjson]

# Vast majority of drugs have 1 testable, 27 have more than 1. All drugs have at least one testable
frequencies(flatten2d([[len(dg['testables']) for dg in d['drugs']] for d in drugjson]))

# Dataframe shape:
# groupid groupname   drugname    drugid  testableid  testablename
# 1 row per testable. Use groupby to restore hierarchy.

# Pandas has a function to help:
drug_df = pd.io.json.json_normalize(
        drugjson,
        # Path to innermost record
        ["drugs", "testables"],
        # Paths to other metadata to extract
        ["id", "name", ["drugs", "id"], ["drugs", "name"]],
        # These prefixes are just to make the column names clear and avoid
        # clashes between the repeated "id" fields.
        meta_prefix="group.",
        record_prefix="group.drugs.testables."
        )
