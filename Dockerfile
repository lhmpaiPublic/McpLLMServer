FROM python:3.12.10-slim

WORKDIR /app

# -----------------------------------------
# 시스템 패키지 (LightGBM 빌드용)
# -----------------------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------
# Python 패키지 설치
# -----------------------------------------
COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -----------------------------------------
# 애플리케이션 복사
# -----------------------------------------
COPY app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "critical", "--no-access-log"]
