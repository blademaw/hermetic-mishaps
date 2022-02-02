# Currently a WIP and a POC; using constrained dictionaries
import pandas as pd
import numpy as np
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
VOWELS = ('a', 'e', 'i', 'o', 'u')

def generate_word(files, seed):
    # set seed
    np.random.seed(seed)

    # acquire base, prefix, and suffix
    pre = pd.read_csv(f"{THIS_FOLDER}/{files[0]}.csv")
    base = pd.read_csv(f"{THIS_FOLDER}/{files[1]}.csv")
    suf = pd.read_csv(f"{THIS_FOLDER}/{files[2]}.csv")
    
    # choose word constituents
    inds = (np.random.randint(len(pre)), np.random.randint(len(base)), np.random.randint(len(suf)))
    prefix = np.random.choice(pre.iloc[inds[0]].unit.split(", "))
    root = np.random.choice(base.iloc[inds[1]].unit.split(", "))
    suffix = np.random.choice(suf.iloc[inds[2]].unit.split(", "))
    const_meaning_arr = (pre.iloc[inds[0]].meaning, base.iloc[inds[1]].meaning, suf.iloc[inds[2]].meaning)
    ex_arr = (pre.iloc[inds[0]].ex, base.iloc[inds[1]].ex, suf.iloc[inds[2]].ex)
    
    # compile word & meaning
    if root[-1] not in VOWELS and suffix[-1] not in VOWELS:
        # add 'o' to separate consonants
        root += 'o'
    
    meaning = " ".join((pre.iloc[inds[0]].meaning, base.iloc[inds[1]].meaning))
    if suf.iloc[inds[2]].end == 1:
        meaning = suf.iloc[inds[2]].meaning + " " + meaning
    else:
        meaning += " " + suf.iloc[inds[2]].meaning

    return (prefix, root, suffix), meaning, const_meaning_arr, ex_arr


# w, m, _, _ = generate_word(("processed_pres", "processed_roots", "processed_sufs"), 123211124)
# print(f"Word:\t{'-'.join(w)}\nLit.\t{m}")