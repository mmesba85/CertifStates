#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 2 ] || die "Usage : run.sh [certificate dir] [threaded|memoization]"

if [ "$2" != "threaded" ] && [ "$2" != "memoization" ]; then
    die "Usage : run.sh [certificate dir] [threaded|memoization]"
fi

DIR=$(dirname $0)
if [ "$DIR" = "." ]; then
    DIR=$(pwd)
fi

printf "\e[1;34mRun parser with file $1\n\e[0m"

cd parser
printf "Installing dependencies ...\n"
npm install
printf "Runing parser ...\n"
node index.js ../$1

printf "\e[1;34mRun checker with $2\n\e[0m"

cd ../checker
if [ "$2" = "threaded" ]; then 
    python3 threaded_check.py ../parser/certificat.json
else 
    python3 threaded_check.py ../parser/Memoization_check.py
fi

printf "\e[1;34mRun collision completer (whois, asn ...)\n\e[0m"
cd ../analysis
python3 collision_completer.py ../checker/collisions.json

