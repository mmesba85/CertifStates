import pandas
import json
from celery import Celery
import os
import threading

DATA_FILE='sample.json'

app = Celery('CheckCol',
             broker='pyamqp://guest@localhost//')

@app.task
def find_duplicates(val, data):
    res = []
    for i, r in data.iterrows():
        if str(r['publicKeyRaw']) == str(val):
            res.append(r.to_dict())
    return res


def process_data():
    f = open('sample.json')
    data = json.load(f)
    res = pandas.DataFrame(data)
    aux = res.transpose()


    d = set()
    for i, r in aux.iterrows():
        v = r['publicKeyRaw']

        if v in d:
            continue
        d.add(v)

        worker = threading.Thread(target=find_duplicates, args=(v, aux))
        worker.start()

        check.append(r.to_dict())
        print(res)