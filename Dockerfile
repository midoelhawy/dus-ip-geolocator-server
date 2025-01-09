FROM python:3.9-slim


WORKDIR /app

RUN apt update && apt install wget curl jq -y
RUN mkdir -p db 

COPY requirements.txt .
COPY lib lib
COPY main.py .
COPY scripts/download-latest-mmdb.sh ./scripts/



RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh .

RUN chmod +x entrypoint.sh
RUN ./scripts/download-latest-mmdb.sh

EXPOSE 5000
CMD ["./entrypoint.sh"]
