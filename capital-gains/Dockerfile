FROM python:3.10-slim

WORKDIR /app

COPY capital-gains/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PORT=8080 

CMD ["python", "app.py"]