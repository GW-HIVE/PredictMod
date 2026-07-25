FROM python:3.12.13-slim

LABEL org.opencontainers.image.title="GSE194040 exploratory pCR expression classifier"
LABEL org.opencontainers.image.description="Reproducible research package for the pooled GSE194040 Elastic Net pCR classifier"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements-lock.txt .
RUN python -m pip install --upgrade pip==25.0.1 \
    && python -m pip install -r requirements-lock.txt

COPY . .

CMD ["python", "scripts/predict_gse194040_single_patient.py", "--help"]
