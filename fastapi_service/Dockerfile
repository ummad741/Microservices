FROM python:3.9

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /fastapp
COPY requirements.txt /fastapp/requirements.txt
RUN pip install -r requirements.txt
COPY . /fastapp/

EXPOSE 8000