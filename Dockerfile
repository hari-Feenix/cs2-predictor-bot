FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["sh", "-c", "python3 discord_bot/main.py & python3 telegram_bot/main.py"]
