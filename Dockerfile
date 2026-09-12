FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y ffmpeg curl unzip git nodejs npm \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deno.land/install.sh | sh

ENV PATH="/root/.deno/bin:${PATH}"

RUN git clone --depth 1 --branch 2.0.0 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git /root/bgutil-ytdlp-pot-provider

WORKDIR /root/bgutil-ytdlp-pot-provider/server

RUN npm ci --no-audit --no-fund \
    && npx tsc

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

CMD ["sh", "-c", "node /root/bgutil-ytdlp-pot-provider/server/build/main.js & gunicorn --bind 0.0.0.0:8080 app:app"]
