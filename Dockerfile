FROM node:26-bookworm-slim AS bgutil

WORKDIR /bgutil

RUN apt-get update \
    && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 --branch 2.0.0 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git .

WORKDIR /bgutil/server

RUN npm ci --no-audit --no-fund \
    && npx tsc


FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y ffmpeg curl unzip nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deno.land/install.sh | sh

ENV PATH="/root/.deno/bin:${PATH}"

COPY --from=bgutil /bgutil/server /root/bgutil-ytdlp-pot-provider/server

COPY requirements.txt .

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

CMD ["sh", "-c", "node /root/bgutil-ytdlp-pot-provider/server/build/main.js & sleep 3 && gunicorn --timeout 120 --bind 0.0.0.0:8080 app:app"]
