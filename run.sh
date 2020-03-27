#!/bin/sh

cd parser
npm install 
node index.js ../$1
cp certificat.json ../checker/sample.json

cd ../checker
python3 threaded_check.py sample.json

cd ../analysis
python3 collision_completer.py ../checker/collisions.json



