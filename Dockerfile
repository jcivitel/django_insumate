FROM python:3.12-alpine AS builder

RUN apk add --no-cache libgcc mariadb-connector-c pkgconf mariadb-dev postgresql-dev linux-headers

WORKDIR /opt/insumate/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /opt/insumate/
COPY manage.py /opt/insumate/
COPY uwsgi.ini /opt/insumate/
COPY entry.sh /opt/insumate/
COPY django_im_api /opt/insumate/django_im_api/
COPY django_im_backend /opt/insumate/django_im_backend/
COPY django_im_frontend /opt/insumate/django_im_frontend/
COPY django_insumate /opt/insumate/django_insumate/

FROM builder AS install
WORKDIR /opt/insumate
ENV VIRTUAL_ENV=/opt/insumate/venv

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir -r /opt/insumate/requirements.txt

FROM install

EXPOSE 8000
CMD ["sh", "entry.sh"]
