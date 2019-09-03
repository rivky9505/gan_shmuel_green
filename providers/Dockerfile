FROM python:latest

WORKDIR /app

RUN mkdir out

RUN pip install XlsxWriter

RUN pip install openpyxl

RUN pip install mysql-connector-python

RUN pip install flask

RUN pip install flask-cors

COPY . /app
 




#RUN pip3 install XlsxWriter
COPY . /app
ENTRYPOINT ["python"]

CMD ["app.py"]
