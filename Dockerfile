# Use official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install Python dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy everything in the repo (core/, discord_bot/, etc.)
COPY . .

# Set working directory to bot folder
WORKDIR /app/discord_bot

# Run the bot
CMD ["python", "main.py"]
