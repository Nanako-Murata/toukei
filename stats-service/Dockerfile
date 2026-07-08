FROM python:3.14-slim

WORKDIR /app

# ★ Azure のヘルスチェックが wget を使うので必須
RUN apt-get update && apt-get install -y wget

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
