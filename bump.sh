#!/bin/sh
# Stamp a new build number into index.html and version.json (run before every commit that changes the app).
b=$(date +%s)
sed -i "s/<meta name=\"pc-build\" content=\"[0-9]*\">/<meta name=\"pc-build\" content=\"$b\">/" index.html
printf '{"build": %s}\n' "$b" > version.json
echo "build $b"
