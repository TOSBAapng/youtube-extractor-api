FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y ffmpeg curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Deno kurulumu
RUN curl -fsSL https://deno.land/install.sh | sh

ENV PATH="/root/.deno/bin:${PATH}"

COPY requirements.txt .

RUN pip install --no-cache-dir -U "yt-dlp[default]" \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
