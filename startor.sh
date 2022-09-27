#!/bin/bash

if [[ $1 == "world" ]]
then
    echo "world"
elif [[ $1 == "us" ]]
then
    echo "us"
else
    echo "Usage: sudo startor.sh world | us"
fi
