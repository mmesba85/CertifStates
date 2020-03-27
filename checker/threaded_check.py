import pandas
import json
import sys
import time
from itertools import product

from concurrent.futures import ProcessPoolExecutor

# check for file entry
if len(sys.argv) < 2:
    print("Missing Argument: Enter file to process")
    exit(1)

DATA_FILE=sys.argv[1]

'''
Find duplicate
Parameter:
    val: key to be searched
    data: dataframe containing the json entry file
Returns:
    Dataframe containing duplicates
'''
def find_duplicates(args):
    val = args[0]
    data = args[1]
    res = data.loc[data['publicKeyRaw'] == val]
 
    return res

'''
Main processing function
 - Convert JSON to Dataframe
 - Iterates over rows
 - For each row, get key value and call find_duplicates
 - Convert all duplicates to JSON
'''
def process_data():
    f = open(DATA_FILE)
    data = json.load(f)
    res = pandas.DataFrame(data)
    aux = res.transpose()

    l = []
    d = set()
    pool = ProcessPoolExecutor(max_workers=40)
    count = 0
    for i, r in aux.iterrows():
        v = r['publicKeyRaw']

        if v in d:
            continue
        d.add(v)
       
        checks = pool.map(find_duplicates, [[v, aux.copy()]] , chunksize=1)
  
        for c in checks:
            if len(c) > 1:
                l.append(c)
                count = count +1
    with open("collisions.json", 'w') as outfile:
        outfile.write(json.dumps([df.transpose().to_dict() for df in l]))
    print("Output in collision.json")
    print("Number of collisions: %d" % count)
            
process_data()