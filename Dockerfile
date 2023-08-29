FROM python:3.8-slim
ENV PYHONUNBUFFERED 1
COPY . /app
WORKDIR /app

RUN apt-get update

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD python manage.py runcrons  && python manage.py runserver 0.0.0.0:8000
