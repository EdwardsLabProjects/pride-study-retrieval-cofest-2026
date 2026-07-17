#!/bin/env python3

import sys, json, os, os.path
from couchws import *

if not len(sys.argv) > 2:
    print("Usage: couch_search_ids.py payload.json ids.txt",file=sys.stderr)
    sys.exit(1)

payload = open(sys.argv[1]).read()
if not os.path.isfile(sys.argv[2]):
    ids = [ sys.argv[2] ]
else:
    ids = open(sys.argv[2]).read().split()
try:
    ids = ids + [ int(i) for i in ids ]
except ValueError:
    pass

all_docs = []
for doc in searchids(payload,ids):
    all_docs.append(doc)

print(json.dumps(all_docs,indent=2))











