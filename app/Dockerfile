FROM python:3-alpine

WORKDIR /app

COPY requirements.txt /app

RUN python3 -m pip install --upgrade pip && python3 -m pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
