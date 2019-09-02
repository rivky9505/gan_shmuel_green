FROM python:latest

COPY . /app

WORKDIR /app

RUN pip install flask mysql-connector-python flask-cors openpyxl

RUN pip install XlsxWriter

RUN pip3 install XlsxWriter

ENTRYPOINT ["python"]

CMD ["app.py"]
