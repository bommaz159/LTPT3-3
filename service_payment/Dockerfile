FROM python:3.9-slim

WORKDIR /app
COPY . /app 

RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y sqlite3

EXPOSE 5001
CMD ["python", "main.py"]
