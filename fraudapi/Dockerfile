FROM python:3.12.12-slim-trixie

ENV PYTHONUNBUFFERED=1

WORKDIR /fraudapi

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY /app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]