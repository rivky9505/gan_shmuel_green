FROM python:latest

WORKDIR /app

RUN mkdir out

RUN pip install XlsxWriter

RUN pip install openpyxl

RUN pip install mysql-connector-python

RUN pip install flask

RUN pip install requests

RUN pip install flask-cors

COPY . /app

ENTRYPOINT ["python"]

CMD ["app.py"]
