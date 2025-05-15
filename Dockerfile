# Use official Python image
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy the whole project
COPY . .

# ✅ Set PYTHONPATH so Python can locate core/
ENV PYTHONPATH="${PYTHONPATH}:/app"

WORKDIR /app/discord_bot

CMD ["python", "main.py"]
