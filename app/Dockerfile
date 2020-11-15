FROM python:3.8

WORKDIR /src/app

RUN apt-get install -y g++ gcc libxml2-dev libxslt-dev libffi-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

COPY . .

CMD ["flask", "run"]
