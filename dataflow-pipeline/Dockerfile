FROM python:3.12.12-slim-trixie

ENV PYTHONUNBUFFERED=1

WORKDIR /dataflow-pipeline

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["python3", "main.py"]