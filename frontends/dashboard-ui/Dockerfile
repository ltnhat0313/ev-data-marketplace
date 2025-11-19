FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Dashboard UI chạy port 8000 trong container (map ra 3000 ở docker-compose cũ nhưng giờ qua nginx thì cứ để 8000)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]