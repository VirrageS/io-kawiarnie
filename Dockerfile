FROM python:3.5
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=settings.production

ADD requirements.txt /app/requirements.txt
WORKDIR /app/
RUN pip install -r requirements.txt
RUN adduser --disabled-password --gecos '' myuser
