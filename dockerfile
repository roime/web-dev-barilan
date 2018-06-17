FROM python:3

COPY . /app
WORKDIR /app
RUN pip3 install flask


CMD ["python", "-u", "web_server.py"]
