FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser . .
RUN mkdir -p /app/instance && chown appuser:appuser /app/instance
USER appuser
VOLUME ["/app/instance"]
EXPOSE 8000

CMD ["python", "app.py"]
