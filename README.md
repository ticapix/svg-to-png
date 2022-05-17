# Convert SVGs to PNGs

A script to convert SVG files to PNG format

It uses Chromium to perform the SVG render and return a data url.

## How to use

Check `test.sh` or

```shell
$ curl -X POST https://svg2png.riphixel.fr/convert/svg2png --data {"svg": "data:image/svg+xml;base64,PHN2ZyBpZD..."}
{
  "height": 972,
  "width": 630,
  "png": "data:image/png;base64,iVBORw0KGg...."
}
```

```shell
curl -X POST https://svg2png.riphixel.fr/convert/svg2png --data @tests/data_sample.json | jq -r .png | cut -d',' -f2 | base64 --decode > test.png
```


## How to deploy

```shell
git remote add clever git+ssh://git@xxxxxx
git push -u clever HEAD:master
```




