#!/bin/bash

# Show figlet fonts w/some lolcat flare

OIFS="$IFS" # Some fonts have spaces in their filenames
IFS=$'\n'

for f in /usr/share/figlet/*.flf; do 
    NAME=$(basename $f .flf)
    echo $NAME
    echo $NAME | figlet -f${NAME} | lolcat
done

IFS=OIFS
