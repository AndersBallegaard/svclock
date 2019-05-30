FROM python:3.7-alpine

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "svclock_server.py" ]