FROM python:3.9-alpine

RUN apk add --no-cache vim build-base tzdata libffi-dev postgresql-dev python3-dev musl-dev curl libjpeg-turbo-dev zlib-dev

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["sh", "/app/entrypoint.sh"]