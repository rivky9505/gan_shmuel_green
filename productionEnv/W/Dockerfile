FROM python:latest

COPY . /app

WORKDIR /app

RUN pip install flask mysql-connector-python flask-cors

ENTRYPOINT ["python"]

CMD ["app.py"]