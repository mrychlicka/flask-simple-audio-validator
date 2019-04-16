FROM ubuntu:18.04

ENV TZ=Europe/Minsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev python3.6-dev python3-tk libsndfile1-dev

COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install wheel
RUN pip3 install sndfile
RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT ["python3"]
CMD ["app/app.py"]

