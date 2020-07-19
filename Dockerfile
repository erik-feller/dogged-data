from alpine:latest
RUN apk add --no-cache --virtual .build-deps build-base g++ python3-dev postgresql-dev && apk add --no-cache --update python3 && pip3 install --upgrade pip setuptools
RUN pip install psycopg2-binary klein
COPY main.py /opt/main.py
COPY lib/ /opt/lib/.
ENTRYPOINT python3 /opt/main.py
