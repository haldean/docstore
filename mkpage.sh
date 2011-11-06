PAGE=$1
CONTENTS=""
if [ -z $PAGE ]; then
  echo "Must specify page name."
  exit
elif [ `redis-cli --raw exists $PAGE` == "1" ]; then
  echo "This page already exists. Loading it into your editor."
  CONTENTS=`redis-cli get $PAGE`
fi

TEMPFILE=`mktemp`
echo $CONTENTS > $TEMPFILE
$EDITOR $TEMPFILE

REMOTE_TEMPFILE=`ssh haldean.org mktemp`
scp $TEMPFILE haldean.org:$REMOTE_TEMPFILE

ssh haldean.org <<EOF
cat $REMOTE_TEMPFILE | redis-cli -x set $PAGE
rm $REMOTE_TEMPFILE
EOF

rm $TEMPFILE
