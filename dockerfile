FROM python

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app ./app
COPY ./dataset ./dataset

WORKDIR /python-docker/app

CMD [ "python", "app.py"]