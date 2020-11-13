FROM python:3.8-alpine

WORKDIR /src/app

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["flask", "run"]