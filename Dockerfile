FROM python:3.8-alpine

WORKDIR /src/app

RUN apk add --no-cache gcc libxml2-dev libxslt-dev musl-dev linux-headers

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

COPY . .

CMD ["flask", "run"]