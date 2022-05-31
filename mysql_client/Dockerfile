FROM python:3.9
#FROM superxi/zerorpc:2.7
#RUN pip install zerorpc==0.6.3
RUN pip install pyzmq==22.3.0
RUN pip install zerorpc

#WORKDIR /usr/src/app

WORKDIR /app
COPY ./common ./
COPY ./mysql_client/ .

#ADD . /mysql_client/
#COPY ./mysql_client/mysql_client.py ./mysql_client.py

#WORKDIR /mysql_client/

