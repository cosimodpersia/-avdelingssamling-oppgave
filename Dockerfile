FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY src/ /app/src/
COPY kilder/ /app/kilder/
USER 65534:65534
CMD ["python", "-m", "incident_lab", "--help"]
