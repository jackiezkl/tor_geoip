#!/bin/bash

if [[ $1 == "world" ]]
then
    echo "world"
elif [[ $1 == "us" ]]
then
    echo "us"
else
    echo -e "Usage:\nsudo startor.sh world | us"
fi
