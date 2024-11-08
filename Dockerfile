FROM ubuntu:22.04
LABEL authors="leo"


ENV TOKEN=''
ENV BLOG_PATH=''
ENV GP_URL=''

RUN apt-get update && \
    apt-get install -y python3-pip python3 nodejs npm && \
    apt-get clean

RUN npm install -g hexo-cli

WORKDIR /app

COPY . .

RUN /usr/bin/pip3 install -r requirement.txt

RUN git config --global user.email "tg@blogerbot.com"
RUN git config --global user.name "tgblogerbot"

