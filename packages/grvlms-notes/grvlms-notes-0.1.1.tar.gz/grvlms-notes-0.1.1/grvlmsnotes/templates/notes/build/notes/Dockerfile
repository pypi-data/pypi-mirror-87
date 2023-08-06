FROM docker.io/ubuntu:18.04

RUN apt update && \
  apt upgrade -y && \
  apt install -y git-core language-pack-en libmysqlclient-dev libssl-dev python python-pip python-virtualenv

# Create python venv
RUN mkdir /openedx/ && virtualenv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install --upgrade pip setuptools

RUN git clone https://github.com/edx/edx-notes-api --branch open-release/ironwood.master --depth 1 /openedx/edx-notes-api
WORKDIR /openedx/edx-notes-api

RUN pip install -r requirements/base.txt

EXPOSE 8000
CMD gunicorn --workers=2 --name notes --bind=0.0.0.0:8000 --max-requests=1000 notesserver.wsgi:application