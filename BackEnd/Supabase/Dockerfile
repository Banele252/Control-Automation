FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /app

RUN pip install --no-cache  -r requirements.txt

COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]

RUN chmod +x /app/entrypoint.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]