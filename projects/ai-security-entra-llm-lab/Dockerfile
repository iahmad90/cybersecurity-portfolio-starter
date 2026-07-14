FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --system app && useradd --system --gid app --create-home app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

USER app

EXPOSE 8000

CMD ["uvicorn", "secure_ai_lab.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]
