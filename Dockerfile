FROM registry.opensource.zalan.do/stups/python:3.5.1-17

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN curl -X PUT --header 'Content-Type: application/json' --header 'Accept: text/html' -d '{
  "api_type": "public",
  "base_url": "public",
  "created": "2015-07-07T15:49:51.230+02:00",
  "doc_url": "public",
  "id": "123",
  "name": "API Registry"
}' 'https://slb-extensibility-demo.appspot.com/APIs/APIRegistry'
COPY app.py /
COPY swagger.yaml /

WORKDIR /
CMD ["python","app.py"]