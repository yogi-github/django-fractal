FROM python:3.7-alpine

RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --no-cache --update python3 python3-dev py3-numpy gcc gfortran musl-dev

WORKDIR /fractal_challenge
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN chmod u+x ./entry.sh
ENTRYPOINT ["./entry.sh"]
