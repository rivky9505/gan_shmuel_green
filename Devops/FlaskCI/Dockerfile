FROM python:latest

COPY . /app

WORKDIR /app

RUN pip install flask flask-cors openpyxl

ENTRYPOINT ["python3"]

CMD ["listening_to_github.py"]
