#!/bin/bash

VAR1=$(sed -n '3p' /etc/tor/torrc)
VAR2="EntryNodes {us} StrictNodes 1"

if [[ $1 == "world" ]]
then
    if [ "$VAR1" = "$VAR2" ]; then
        sed '3,5 s/StrictNodes 1/StrictNodes 0/' /etc/tor/torrc
        tor
    else
        echo "It's already in the World mode"
        tor
    fi
elif [[ $1 == "us" ]]
then
    if [ "$VAR1" = "$VAR2" ]; then
        echo "It's already in the US mode"
        tor
    else

        sed '3,5 s/StrictNodes 1/StrictNodes 1/' /etc/tor/torrc
        tor
    fi
else
    echo -e "Usage:\nsudo startor.sh world | us"
fi
