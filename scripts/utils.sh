HOST="haldean.org"

upload() {
  PAGE=$1
  FILE=$2

  REMOTE_TEMPFILE=`ssh $HOST mktemp`
  scp $FILE $HOST:$REMOTE_TEMPFILE

  ssh $HOST <<EOF
cat $REMOTE_TEMPFILE | redis-cli -x set $PAGE
rm $REMOTE_TEMPFILE
EOF
}

remredis() {
  ssh $HOST "redis-cli $@"
}

