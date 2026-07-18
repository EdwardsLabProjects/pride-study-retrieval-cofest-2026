BASEURL = "https://edwardslab.bmcb.georgetown.edu/~nedwards/dropbox/6ItUS2tEdC/"
GITHUB = "https://raw.githubusercontent.com/EdwardsLabProjects/pride-study-retrieval-cofest-2026/refs/heads/main/data/"

import os, os.path, subprocess
import pandas

def download_embeddings(model="openai-3-small"):
    # files...
    csvfile = f"pride-embeddings-{model}.csv"
    fthfile = f"pride-embeddings-{model}.fth"
    for f in [csvfile, fthfile]:
      if not os.path.exists(f):
        subprocess.run(["wget", BASEURL+f])
    return csvfile, fthfile

def download_knownstudies():
    trueposfile = "truepos.txt"
    truenegfile = "trueneg.txt"
    for f in [trueposfile, truenegfile]:
      if not os.path.exists(f):
        subprocess.run(["wget", GITHUB+f])
    return trueposfile,truenegfile

import numpy as np
import pandas as pd
import random

def set_random_seed(state=None):
    if not state:
        state = random.randint(1,10000000)

    print(f"Using random seed: {state}")

    # Seeds all scikit-learn functions that default to random_state=None
    np.random.seed(state)
    random.seed(state)

def embeddings(model="openai-3-small"):
    csvfile,fthfile = download_embeddings(model)
    emb = pd.read_feather(fthfile)
    md = pd.read_csv(csvfile)
    return md,emb

def knownstudies():
    trueposfile,truenegfile = download_knownstudies()
    tp = set(open(trueposfile).read().split())
    tn = set(open(truenegfile).read().split())
    assert len(set(tp) & set(tn)) == 0, "TP and TN should not intersect!"
    return tp,tn

VERSION='1.0.1'
print(f"Version: {VERSION}")

   