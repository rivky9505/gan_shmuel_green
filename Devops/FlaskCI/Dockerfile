FROM python:latest

COPY . /app

WORKDIR /app

RUN pip install flask flask-cors openpyxl

#ENTRYPOINT ["sudo", "python3"]

CMD ["sudo", "python3", "listening_to_github.py"]
