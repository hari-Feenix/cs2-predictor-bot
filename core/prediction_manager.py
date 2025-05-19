import sqlite3
from datetime import datetime

class PredictionManager:
    def __init__(self, db_path='predictions.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                user_id TEXT,
                match_id TEXT,
                predicted_winner TEXT,
                team1 TEXT,
                team2 TEXT,
                match_time TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                user_id TEXT PRIMARY KEY,
                score INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_prediction(self, user_id, match_id, predicted_winner, match_info):
        team1 = match_info.get('team1', '')
        team2 = match_info.get('team2', '')
        match_time = match_info.get('time', '')
        self.cursor.execute(
            "INSERT INTO predictions VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, match_id, predicted_winner, team1, team2, match_time)
        )
        self.conn.commit()

    def get_predictions(self):
        return self.cursor.execute("SELECT user_id, match_id, predicted_winner FROM predictions").fetchall()

    def get_match_info(self, match_id):
        row = self.cursor.execute(
            "SELECT team1, team2, match_time FROM predictions WHERE match_id=? LIMIT 1", (match_id,)
        ).fetchone()
        if row:
            team1, team2, match_time = row
            try:
                match_time = datetime.fromisoformat(match_time.replace('Z', '+00:00'))
            except:
                match_time = None
            return {"team1": team1, "team2": team2, "time": match_time}
        return {}

    def delete_prediction(self, user_id, match_id):
        self.cursor.execute("DELETE FROM predictions WHERE user_id=? AND match_id=?", (user_id, match_id))
        self.conn.commit()

    def increment_score(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO scores (user_id, score) VALUES (?, 0)", (user_id,))
        self.cursor.execute("UPDATE scores SET score = score + 1 WHERE user_id=?", (user_id,))
        self.conn.commit()

    def get_leaderboard(self):
        return self.cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10").fetchall()
