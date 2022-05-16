# Convert SVGs to PNGs

A script to convert SVG files to PNG format

This script preserves base64 encoded image data

It also converts handcoded SVG markup to PNG

It uses Chromium to perform the SVG render and saves it


## To install:
* You will need Chrome or Chromium
* You will need Python's Selenium drivers to make this work

## To Run:
`./svg-to-png-using-chromium.py $FILE_PATH`

## Docker

`docker build -f Dockerfile --tag svg2png:latest .`

`docker run --rm -it -p 5000:4142 svg2png:latest`

docker build -f Dockerfile --tag svg2png:latest . && docker run --rm -it -p 4142:5000 svg2png:latest

## Test

curl -X POST http://127.0.0.1:4142/convert/svg2png --data @data_sample.json

curl -X POST http://127.0.0.1:5000/convert/svg2png2 --data "{\"svg\": \"data:image/svg+xml;base64,`cat diagram2.svg | base64 --wrap=0`\"}"
curl -X POST http://127.0.0.1:5000/convert/svg2png --data "{\"svg\": \"data:image/svg+xml;base64,`cat diagram1.svg | base64 --wrap=0`\"}" | base64 --decode > diagram1.png

