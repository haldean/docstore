upload() {
  PAGE=$1
  FILE=$2

  REMOTE_TEMPFILE=`ssh haldean.org mktemp`
  scp $FILE haldean.org:$REMOTE_TEMPFILE

  ssh haldean.org <<EOF
cat $REMOTE_TEMPFILE | redis-cli -x set $PAGE
rm $REMOTE_TEMPFILE
EOF
}

remredis() {
  ssh haldean.org "redis-cli $@"
}

