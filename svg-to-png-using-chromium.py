#!/usr/bin/env python3

from flask import Flask, request
from selenium import webdriver
import json
import base64
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def send(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd':cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')


@app.route('/convert/svg2png', methods=['POST'])
def svg2png():
    print(request.headers)
    body = request.get_json(force=True)
    assert 'svg' in body, "No 'svg' parameter in body"
    svgsrc = body['svg']
    options = webdriver.ChromeOptions()
    # to run in container
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-infobars")

    desired_dpi = 2.0
    options.add_argument(f"--force-device-scale-factor={desired_dpi}")

    driver = webdriver.Chrome(options=options)
    print(svgsrc[:32])
    driver.get(svgsrc)

    # take screenshot with a transparent background
    send(driver, "Emulation.setDefaultBackgroundColorOverride", {
        'color': {'r': 0, 'g': 0, 'b': 0, 'a': 0}
    })
    elt = driver.find_element(by=webdriver.common.by.By.TAG_NAME, value="svg")

    # print(elt.rect)
    # print('Window position', driver.get_window_position())
    # print('Window size', driver.get_window_size())

    # # driver.execute_script("arguments[0].style.transform='scale(1.0, 1.0)';", elt)
    driver.set_window_size(elt.size['width']+1, elt.size['height']+1)

    # image = elt.screenshot_as_png
    driver.save_screenshot("screenshot.png")
    bin = open('screenshot.png', 'rb').read()
    driver.quit()
    return b"data:image/png;base64," + base64.b64encode(bin)
    # return b"data:image/png;base64," + base64.b64encode(image)


if __name__ == '__main__':
    # run app in debug mode on port 8080
    app.run(debug=True, host="0.0.0.0", port=8080)
