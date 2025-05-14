import sqlite3
from .hltv_results import fetch_completed_results

class PredictionManager:
    def __init__(self, db_path='predictions.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    user_id TEXT,
                    match_id TEXT,
                    prediction TEXT,
                    PRIMARY KEY (user_id, match_id)
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS scores (
                    user_id TEXT PRIMARY KEY,
                    score INTEGER DEFAULT 0
                )
            ''')

    def add_prediction(self, user_id, match_id, predicted_winner):
        with self.conn:
            self.conn.execute('''
                INSERT OR REPLACE INTO predictions (user_id, match_id, prediction)
                VALUES (?, ?, ?)
            ''', (str(user_id), match_id, predicted_winner))

    def get_leaderboard(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id, score FROM scores ORDER BY score DESC LIMIT 10")
        return cursor.fetchall()

    async def update_results(self, bot):
        completed_matches = fetch_completed_results()
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id, match_id, prediction FROM predictions")
        all_predictions = cursor.fetchall()

        for user_id, match_id, predicted in all_predictions:
            if match_id in completed_matches:
                actual = completed_matches[match_id]
                user = await bot.fetch_user(int(user_id))
                if predicted == actual:
                    with self.conn:
                        self.conn.execute('''
                            INSERT INTO scores (user_id, score)
                            VALUES (?, 1)
                            ON CONFLICT(user_id) DO UPDATE SET score = score + 1
                        ''', (user_id,))
                    await user.send(f"✅ Correct prediction for {match_id}: {actual}")
                else:
                    await user.send(f"❌ Wrong prediction for {match_id}. {actual} won.")
                with self.conn:
                    self.conn.execute("DELETE FROM predictions WHERE user_id=? AND match_id=?", (user_id, match_id))
