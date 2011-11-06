source utils.sh

PAGE=$1

if [ $# -eq 2 ]; then
  upload $1 $2
  exit
fi

CONTENTS=""
if [ -z $PAGE ]; then
  echo "Must specify page name."
  exit
elif [ `remredis --raw exists $PAGE` == "1" ]; then
  echo "This page already exists. Loading it into your editor."
  CONTENTS=`remredis get $PAGE`
fi

TEMPFILE=`mktemp`
echo $CONTENTS > $TEMPFILE
$EDITOR $TEMPFILE

upload $PAGE $TEMPFILE

rm $TEMPFILE
