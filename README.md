# Convert SVGs to PNGs

A script to convert SVG files to PNG format

It uses Chromium to perform the SVG render and return a data url.

## How to use

Check `test.sh` or

`curl -X POST https://svg2png.riphixel.fr/convert/svg2png --data @tests/data_sample.json | cut -d',' -f2 | base64 --decode > test.png`

## How to update service

`git push -u clever master`

