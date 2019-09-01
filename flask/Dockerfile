FROM jfloff/alpine-python
WORKDIR /provider-api
COPY . .
RUN pip3 install flask mysql-connector-python flask-cors
CMD python3 provider.py
