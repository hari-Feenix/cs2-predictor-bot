class PredictionManager:
    def __init__(self):
        self.predictions = {}  # {user_id: {match_id: 'TeamName'}}
        self.scores = {}       # {user_id: score}

    def add_prediction(self, user_id, match_id, predicted_winner):
        if user_id not in self.predictions:
            self.predictions[user_id] = {}
        self.predictions[user_id][match_id] = predicted_winner

    async def update_results(self, bot):
        # This is a placeholder. You'd scrape results from HLTV.
        # For demo purposes, we'll just simulate it.
        completed_matches = {
            '123456': 'Team A',
            '789012': 'Team B',
        }

        for user_id, user_preds in self.predictions.items():
            for match_id, predicted in user_preds.items():
                if match_id in completed_matches:
                    actual = completed_matches[match_id]
                    if predicted == actual:
                        self.scores[user_id] = self.scores.get(user_id, 0) + 1
                        user = await bot.fetch_user(user_id)
                        await user.send(f"✅ You predicted {predicted} and were correct! (+1 point)")
                    else:
                        user = await bot.fetch_user(user_id)
                        await user.send(f"❌ You predicted {predicted} but {actual} won.")

            # Remove evaluated predictions
            for match_id in completed_matches:
                self.predictions[user_id].pop(match_id, None)
