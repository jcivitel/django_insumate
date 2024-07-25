FROM python:3.12-alpine AS builder

RUN apk add --no-cache libgcc mariadb-connector-c pkgconf mariadb-dev \
    postgresql-dev linux-headers zbar-dev jpeg-dev zlib-dev musl-dev gcc

WORKDIR /opt/insumate/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /opt/insumate/

FROM builder AS install
WORKDIR /opt/insumate
ENV VIRTUAL_ENV=/opt/insumate/venv

RUN python -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir -r /opt/insumate/requirements.txt

FROM install

EXPOSE 8000
CMD ["sh", "entry.sh"]
