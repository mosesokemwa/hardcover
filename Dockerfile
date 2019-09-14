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

COPY requirements.txt /requirements.txt
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
LABEL Name=hardcover Version=0.0.1
COPY --from=builder /install /usr/local
COPY . /app
# EXPOSE 3000
RUN apk update && apk upgrade \
    && apk add --update --no-cache \
      --virtual .build-deps \
      libffi-dev build-base jpeg-dev libpng-dev postgresql-dev \
    && apk add --update --no-cache libffi jpeg postgresql \
    && apk del --purge .build-deps \
    && rm -rf /var/cache/apk/*

RUN pip install psycopg2-binary

WORKDIR /app
# CMD ["gunicorn", "-w 4", "main:app"]
CMD ["python3", "-m", "hardcover"]
