FROM python:3.9
#FROM superxi/zerorpc:2.7
#RUN pip install zerorpc==0.6.3
RUN pip install pyzmq==22.3.0
RUN pip install zerorpc
RUN pip install requests

#RUN pip install zerorpc

#RUN pip install --no-cache-dir websocket-client
#RUN [ "cp", "../common/exchange.py", "/mktdata/" ]
#ADD ../common/exchange.py /mktdata/
#ADD ../common/symbol.py /mktdata/
#ADD mktdata.py /mktdata/

WORKDIR /app
COPY ./common ./
COPY ./mktdata/ .

#CMD ["python3", "-u", "./mktdata.py"]
#WORKDIR /
#WORKDIR /mktdata/

