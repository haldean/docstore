source $(dirname `pwd`/$0)/utils.sh

PAGE=$1
if [ -z $PAGE ]; then
  echo "Must specify page name."
  exit
fi

if [ `remredis --raw exists $PAGE` == "0" ]; then
  echo "That page doesn't exist. Exiting."
  exit
fi

read -p "About to delete $PAGE. Are you sure? [y/N] " -n 1
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  if [ `remredis del $PAGE` == "1" ]; then
    remredis srem pages $PAGE
    remredis del $PAGE_views
    echo Success.
  else
    echo Failed.
  fi
fi
