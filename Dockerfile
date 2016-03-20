FROM python:3.5

ENV C_FORCE_ROOT 1

RUN adduser --disabled-password --gecos '' docker

RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/.
EXPOSE 8000

CMD ["./app/start-web.sh"]
