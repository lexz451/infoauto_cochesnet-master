#!/bin/sh


set -o errexit
set -o nounset


npm set progress=false
rm -rf package-lock.json
npm install
bower install
npm rebuild node-sass

exec "$@"









