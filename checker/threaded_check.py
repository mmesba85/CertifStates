import pandas
import json
from celery import Celery
import os
from threading import Thread

DATA_FILE='sample.json'

app = Celery('CheckCol',
             broker='pyamqp://guest@localhost//')


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return



def find_duplicates(val, data, row):
    column_names = list(data.columns.values)
    res = pandas.DataFrame(columns=column_names)
    for i, r in data.iterrows():
        if str(r['publicKeyRaw']) == str(val):
            if not r.equals(row):
                res.loc[len(res)] = r
    return res


def process_data():
    f = open('sample.json')
    data = json.load(f)
    res = pandas.DataFrame(data)
    aux = res.transpose()

    l = []
    d = set()
    for i, r in aux.iterrows():
        v = r['publicKeyRaw']

        if v in d:
            continue
        d.add(v)
        worker = ThreadWithReturnValue(target=find_duplicates, args=(v, aux, r))
        worker.start()
        check = worker.join()
        if not check.empty:
            check.loc[len(check)] = r
            l.append(check)
    return l
            

process_data()