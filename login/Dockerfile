FROM python:3.9-alpine3.15

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN pip install -r requirements.txt

COPY ./app .

EXPOSE 5000

ENTRYPOINT ["python3", "login.py"]