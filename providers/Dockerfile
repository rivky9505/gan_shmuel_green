FROM python:latest



WORKDIR /app

RUN pip install flask

RUN pip install mysql-connector-python

RUN pip install flask-cors

RUN pip install openpyxl

RUN pip install XlsxWriter

#RUN pip3 install XlsxWriter
COPY . /app
ENTRYPOINT ["python"]

CMD ["app.py"]
