#!/usr/bin/env python3

from argparse import ArgumentParser
from selenium import webdriver
import json, os
# from PIL import Image

parser = ArgumentParser(
    description='Convert SVGs to PNGs'
)

parser.add_argument(
    'file',
    help=
    'The Path of the svg',
    nargs='?'
)

parser.add_argument('--out', '-o', type=str)
parser.add_argument('--width', '-w', type=int)

args = parser.parse_args()

width = args.width if args.width else 64

def send(cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd':cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1420,1080')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--disable-infobars")
driver = webdriver.Chrome(options=options)

driver.get("file:///" + os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'wrap.html')
)

svgfile = "file:///" + os.path.join(
    os.path.dirname(os.path.realpath(__file__)), args.file)

width = 1080

driver.execute_script('showImage("%s", "%s")' % (svgfile, width))

path = os.path.join(os.getcwd(), args.file)

out = args.out if args.out else args.file[:-4] + '.png'


# take screenshot with a transparent background
send("Emulation.setDefaultBackgroundColorOverride", {
    'color': {'r': 0, 'g': 0, 'b': 0, 'a': 0}
})
image = driver.find_element_by_id("svg").screenshot_as_png
send("Emulation.setDefaultBackgroundColorOverride")  # restore
driver.quit()

with open(out, 'wb') as fd:
    fd.write(image)

