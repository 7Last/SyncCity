FROM python:3.11.9-alpine
WORKDIR /simulator
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
CMD ["python3","main.py"]