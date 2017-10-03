#!/bin/bash

set -e

host="$1"

until pg_isready; do
    >$2 echo "Postgres is not running yet - retrying"
    sleep 1
done

exit $?