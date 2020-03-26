import pandas
import json
import syssss
from concurrent.futures import ThreadPoolExecutor

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
def find_duplicates(val, data, row):
    column_names = list(data.columns.values)
    res = data.loc[data['publicKeyRaw'] == val]
    return res

'''
Main processing function
 - Convert JSON to Dataframe
 - Iterates over rows
 - For each row, get key value and call find_duplicates
 - Convert all duplicates to JSON file
'''
def process_data():
    f = open(DATA_FILE)
    data = json.load(f)
    res = pandas.DataFrame(data)
    aux = res.transpose()

    l = []
    d = set()
    pool = ThreadPoolExecutor(40)
    for i, r in aux.iterrows():
        v = r['publicKeyRaw']

        if v in d:
            continue
        d.add(v)
       
        check = pool.submit(find_duplicates, v, aux, r)
        
        res = check.result()
        if not res.empty:
            if res.shape[0] == 1:
                continue
            l.append(res)
           
    with open("collisions.json", 'w') as outfile:
        outfile.write(json.dumps([df.transpose().to_dict() for df in l]))

            
process_data()