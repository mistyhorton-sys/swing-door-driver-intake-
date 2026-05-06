FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && \
    uv export --frozen --no-dev --format requirements-txt -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000", "--proxy-headers"]
