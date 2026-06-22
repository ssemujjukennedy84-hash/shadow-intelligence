FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir numpy==1.24.3 pandas==2.0.3
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "shadow_web:app"]
