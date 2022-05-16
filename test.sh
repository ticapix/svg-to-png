#!/bin/sh

set +ex

for json in tests/*.json; do
    png=${json%%.json}.png
    echo "$json -> $png"
    rm $png
    curl -X POST http://127.0.0.1:5000/convert/svg2png --data @$json | cut -d',' -f2 | base64 --decode > $png
done

for svg in tests/*.svg; do
    png=${svg%%.svg}.png
    echo "$svg -> $png"
    rm $png
    curl -X POST http://127.0.0.1:5000/convert/svg2png --data "{\"svg\": \"data:image/svg+xml;base64,`cat $svg | base64 --wrap=0`\"}" | cut -d',' -f2 | base64 --decode > $png
done
