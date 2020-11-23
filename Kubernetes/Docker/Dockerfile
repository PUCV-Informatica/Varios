FROM python:3.8

MAINTAINER "diego.tapia.r@mail.pucv.cl"

RUN mkdir -p /workspace
WORKDIR /workspace
COPY requirements.txt /workspace
RUN pip install -r requirements.txt
RUN rm requirements.txt
RUN git clone -b master https://rootchile:{TOKEN}@github.com/rootchile/MagisterTesis.git .

CMD ["python","main.py"]