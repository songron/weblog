#!/bin/sh
echo "Usage: $0 [-s src_dir] [-d dst_dir]"
SRCDIR=webpage
DSTDIR=text
#set -- $(getopt s:d: "$@")
while [ $# -gt 0 ]
do
  if [ "$1" == "-s" ] ;then
    SRCDIR=$2
  elif [ "$1" == "-d" ] ;then
    DSTDIR=$2
  fi
  shift
done
echo "SRCDIR=$SRCDIR"
echo "DSTDIR=$DSTDIR"
mkdir -p $DSTDIR
# 处理当前目录
FILES=$(ls $SRCDIR)
for FILE in $FILES; do
  if [ -f "$SRCDIR/$FILE" ]; then
    ./html2text.py $SRCDIR/$FILE | sed '/^[[:space:]]*$/d' > $DSTDIR/$FILE.txt&
  fi
done
# 处理子目录
DIRS=$(ls $SRCDIR)
for DIR in $DIRS; do
  if [ -d "$SRCDIR/$DIR" ]; then
    mkdir -p $DSTDIR/$DIR
    FILES=$(ls $SRCDIR/$DIR)
    for FILE in $FILES; do
      ./html2text.py $SRCDIR/$DIR/$FILE | sed '/^[[:space:]]*$/d' > $DSTDIR/$DIR/$FILE.txt&
    done
  fi
done
