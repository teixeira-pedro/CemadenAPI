FROM python:3.10-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir cemadem_app
COPY . cemadem_app/

ENTRYPOINT ["tail", "-f", "/dev/null"]
