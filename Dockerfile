# # Python support can be specified down to the minor or micro version
# # (e.g. 3.6 or 3.6.3).
# # OS Support also exists for jessie & stretch (slim and full).
# # See https://hub.docker.com/r/library/python/ for all supported Python
# # tags from Docker Hub.
# FROM python:alpine

# # If you prefer miniconda:
# #FROM continuumio/miniconda3

# LABEL Name=hardcover Version=0.0.1
# EXPOSE 3000

# WORKDIR /app
# ADD . /app

# # Using pip:
# RUN python3 -m pip install -r requirements.txt
# CMD ["python3", "-m", "hardcover"]


FROM python:alpine as base
FROM base as builder
RUN mkdir /install
WORKDIR /install

COPY ./requirements.txt /var/www/hardcover/requirements.txt
RUN apk --update --upgrade add gcc postgresql-dev \
  musl-dev jpeg-dev zlib-dev \
  libffi-dev cairo-dev pango-dev \
  gdk-pixbuf-dev postgresql-dev \
  python3-dev
RUN apk --update --upgrade add gcc \
  musl-dev jpeg-dev zlib-dev \
  libffi-dev cairo-dev pango-dev \
  gdk-pixbuf-dev python3-dev
RUN pip install --install-option="--prefix=/install" -r /var/www/hardcover/requirements.txt

FROM base
LABEL Name=hardcover Version=0.0.1
COPY --from=builder /install /usr/local
COPY . /app
RUN apk update && apk upgrade \
  && apk add --update --no-cache \
  --virtual .build-deps \
  libffi-dev build-base jpeg-dev libpng-dev postgresql-dev \
  && apk add --update --no-cache libffi jpeg postgresql \
  && apk del --purge .build-deps \
  && rm -rf /var/cache/apk/*

RUN apk --update --upgrade add gcc \
  musl-dev jpeg-dev zlib-dev \
  libffi-dev cairo-dev pango-dev \
  gdk-pixbuf-dev python3-dev

RUN pip install psycopg2-binary

WORKDIR /app
EXPOSE 5000
CMD ["flask" "run" "-h 0.0.0.0"]

