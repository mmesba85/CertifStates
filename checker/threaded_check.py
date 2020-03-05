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
        worker = ThreadWithReturnValue(target=find_duplicates, args=(v, aux))
        worker.start()
        check = worker.join()

        check.append(r.to_dict())
        print(res)

process_data()