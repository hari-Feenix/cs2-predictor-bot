# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy the entire project (core, discord_bot, etc.)
COPY . .

# Move into the bot folder
WORKDIR /app/discord_bot

# Run the bot
CMD ["python", "main.py"]
