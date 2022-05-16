FROM python:3-bullseye

# Identify the maintainer of an image
LABEL maintainer="pierre@gronlier.fr"
 
# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

ADD ./requirements.txt .
RUN pip install -Ur requirements.txt

ADD ./svg-to-png-using-chromium.py .

EXPOSE 5000
ENTRYPOINT ["python3", "./svg-to-png-using-chromium.py"]
