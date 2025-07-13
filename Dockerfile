FROM python:3.10.5

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
