#!/bin/sh

set -ex

docker build -f Dockerfile --tag svg2png:latest .

docker stop svg2png || true
docker rm svg2png || true

# docker run -d --name svg2png -p 8080:3000 svg2png:latest
docker run -d --name svg2png svg2png:latest
docker logs --follow svg2png &

sleep 2

host=http://`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' svg2png`:8080

echo found docker running at $host

for json in tests/*.json; do
    png=${json%%.json}.png
    echo "$json -> $png"
    rm $png || true
    curl -X POST $host/convert/svg2png --data @$json | jq -r .png | cut -d',' -f2 | base64 --decode > $png
done

for svg in tests/*.svg; do
    png=${svg%%.svg}.png
    echo "$svg -> $png"
    rm $png || true
    curl -X POST $host/convert/svg2png --data "{\"svg\": \"data:image/svg+xml;base64,`cat $svg | base64 --wrap=0`\"}" | jq -r .png | cut -d',' -f2 | base64 --decode > $png
done

docker stop svg2png
docker rm svg2png
