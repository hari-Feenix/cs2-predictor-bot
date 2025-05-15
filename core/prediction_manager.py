import sqlite3

class PredictionManager:
    def __init__(self, db_path='predictions.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                user_id TEXT,
                match_id TEXT,
                predicted_winner TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                user_id TEXT PRIMARY KEY,
                score INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_prediction(self, user_id, match_id, predicted_winner):
        self.cursor.execute("INSERT INTO predictions VALUES (?, ?, ?)", (user_id, match_id, predicted_winner))
        self.conn.commit()

    def get_predictions(self):
        return self.cursor.execute("SELECT * FROM predictions").fetchall()

    def delete_prediction(self, user_id, match_id):
        self.cursor.execute("DELETE FROM predictions WHERE user_id=? AND match_id=?", (user_id, match_id))
        self.conn.commit()

    def increment_score(self, user_id):
        self.cursor.execute("INSERT OR IGNORE INTO scores (user_id, score) VALUES (?, 0)", (user_id,))
        self.cursor.execute("UPDATE scores SET score = score + 1 WHERE user_id=?", (user_id,))
        self.conn.commit()

    def get_leaderboard(self):
        return self.cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10").fetchall()
