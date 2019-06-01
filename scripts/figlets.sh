#!/bin/bash

# Show figlet fonts w/some lolcat flare

for f in /usr/share/figlet/*.flf; do 
    echo $(basename $f .flf) | figlet -f$(basename $f .flf) | lolcat 
done
