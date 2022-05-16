#!/usr/bin/env python3

from flask import Flask, request
from selenium import webdriver
import json, os
import base64
from flask_cors import CORS


def send(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd':cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')

app = Flask(__name__)
CORS(app)


@app.route('/convert/svg2png', methods=['POST'])
def svg2png():
    body = request.get_json(force=True)
    assert 'svg' in body, "No 'svg' parameter in body"
    svgsrc = body['svg']
    width = body.get('width', '1080')
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1420,1080')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-infobars")

    # for PDF
    settings = {
       "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2
    }
    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--kiosk-printing')

    driver = webdriver.Chrome(options=options)

    driver.get("file:///" + os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'wrap.html')
    )

    driver.execute_script('showImage("%s", "%s")' % (svgsrc, width))

    # take screenshot with a transparent background
    send(driver, "Emulation.setDefaultBackgroundColorOverride", {
        'color': {'r': 0, 'g': 0, 'b': 0, 'a': 0}
    })
    image = driver.find_element_by_id("svg").screenshot_as_png
    send(driver, "Emulation.setDefaultBackgroundColorOverride")  # restore

    driver.execute_script('window.print();') # convert to PDF
    driver.quit()
    return b"data:image/png;base64, " + base64.b64encode(image)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
