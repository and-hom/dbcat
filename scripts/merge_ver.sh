#!/bin/sh

branch=$(git rev-parse --symbolic --abbrev-ref HEAD)
if [ "develop" = "$branch" ]
then
    return 0
else
    return 1
fi