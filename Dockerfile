FROM python:3

WORKDIR /var/www/hardcover

COPY ./requirements.txt /var/www/hardcover/requirements.txt
RUN \
  pip install -r /var/www/hardcover/requirements.txt

COPY . /var/www/hardcover
