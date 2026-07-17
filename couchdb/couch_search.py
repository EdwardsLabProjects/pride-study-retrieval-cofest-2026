#!/bin/env python3

import sys, json
from couchws import *

if len(sys.argv) < 2:
    print("Usage: couch_search.py payload.json",file=sys.stderr)
    sys.exit(1)

payload = open(sys.argv[1]).read()

all_docs = []
for doc in search(payload):
    all_docs.append(doc)

# print(json.dumps(all_docs,indent=2))

# print("Get pride entry by _id")
# id = all_docs[0]["_id"]
# response = get(id)
# print(json.dumps(response,indent=2))

















