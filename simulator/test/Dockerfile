FROM python:3.11.9-alpine
WORKDIR /simulator/test
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#CMD ["pytest", "-c", "pytest.ini"]