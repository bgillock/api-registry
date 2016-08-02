FROM registry.opensource.zalan.do/stups/python:3.5.1-17

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY app.py /
COPY swagger.yaml /

WORKDIR /
CMD ["python","app.py"]