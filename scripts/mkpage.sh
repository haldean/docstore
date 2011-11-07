source ./utils.sh

PAGE=$1

if [ $# -eq 2 ]; then
  upload $1 $2
  exit
fi

TEMPFILE=`mktemp`
if [ -z $PAGE ]; then
  echo "Must specify page name."
  exit
elif [ `remredis --raw exists $PAGE` == "1" ]; then
  echo "This page already exists. Loading it into your editor."
  remredis --raw get $PAGE > $TEMPFILE
fi

$EDITOR $TEMPFILE

upload $PAGE $TEMPFILE
remredis sadd pages $PAGE

rm $TEMPFILE
