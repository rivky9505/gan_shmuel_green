FROM python:3.7.4-slim
RUN pip install requests
RUN pip install datetime
WORKDIR /endtoend 
COPY . .
RUN chmod +x testinit.bash
ENTRYPOINT bash