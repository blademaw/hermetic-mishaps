# File to process dictionaries for use in hermes.py
import pandas as pd
import numpy as np
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
ARTICLE_ENDERS = ('a', 'to', 'the', 'one', 'an', 'verb')

def process_dicts(files, delim):
    """Function to attempt to process dictionaries given files.
    
    Input: iterable of .txt files without file extension
    Output: 1 if successfully saves new files, 0 else
    
    :precondition: txt has three headers of correct interpretation,
                    multiple entries of units are sep'd by comma"""
    for unit_ind, file_name in enumerate(files):
        # load the dictionary into a dataframe, for now use set headers
        df = pd.read_table(f"{THIS_FOLDER}/{file_name}.txt", header=None, delimiter=delim).set_axis(["unit", "meaning", "ex"], axis=1, inplace=False)
        max_ind = len(df) + 1

        # for each entry
        for loc_no in range(len(df)):
            # replace hyphens
            df.loc[df.unit == df.iloc[loc_no].unit, 'unit'] = df.iloc[loc_no].unit.strip().replace("-", "")

            # step 1 - if multiple defs exist, split
            unit_arr = df.iloc[loc_no].unit.split(", ")
            meaning_arr = df.iloc[loc_no].meaning.split("; ")
            if len(unit_arr) > 1 and len(unit_arr) == len(meaning_arr):
                # independent definitions, add new rows
                for i, unit_def in enumerate(unit_arr[1:], start=1):
                    df.loc[max_ind] = [unit_def, meaning_arr[i], df.iloc[loc_no].ex]
                    max_ind += 1
                
                # keep only first def
                df.iloc[loc_no, [0, 1]] = [unit_arr[0], meaning_arr[0]]
            
        # if dealing with suffixes, add placement column
        if unit_ind == 2:
            df.loc[:, 'end'] = pd.Series(np.repeat(0, len(df)), index=df.index)
            for loc_no in range(len(df)):
                unit = df.iloc[loc_no].meaning.split(" ")[0]
                if unit[len(unit)-3:] == 'ing' or unit in ARTICLE_ENDERS:
                    df.iloc[loc_no, 3]= 1
        
        # write to new csv
        df.to_csv(f"{THIS_FOLDER}/processed_{file_name}.csv", index=False)

            

process_dicts(["pres", "roots", "sufs"], '\t')