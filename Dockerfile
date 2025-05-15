# Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy all folders (not just discord_bot)
COPY . .

WORKDIR /app/discord_bot

CMD ["python", "main.py"]
