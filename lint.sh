#!/bin/sh
for FILE in addons/*
do
  if [[ -d $FILE ]]; then
    echo `basename $FILE`
    web-ext lint -s addons/`basename $FILE`
  fi
done