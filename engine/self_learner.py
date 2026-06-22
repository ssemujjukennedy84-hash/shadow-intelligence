"""
Self-Learning Engine - Adjusts Sun Tzu chapter weights based on news + market data
"""

import json
import os
import requests
from datetime import datetime, timedelta
import hashlib

class SelfLearner:
    def __init__(self, weights_file="weights.json"):
        self.weights_file = weights_file
        self.weights = self.load_weights()
        self.history_file = "prediction_history.json"
        self.history = self.load_history()
        self.news_api_key = os.environ.get("NEWS_API_KEY", "")
        
    def load_weights(self):
        if os.path.exists(self.weights_file):
            with open(self.weights_file, 'r') as f:
                return json.load(f)
        return {f"chapter_{i:02d}": 1.0 for i in range(1, 14)}
    
    def save_weights(self):
        with open(self.weights_file, 'w') as f:
            json.dump(self.weights, f, indent=2)
    
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def fetch_news(self, symbol, days=3):
        if not self.news_api_key:
            return self.fallback_news(symbol)
        url = f"https://newsapi.org/v2/everything?q={symbol}&from={(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')}&sortBy=relevancy&apiKey={self.news_api_key}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                articles = r.json().get("articles", [])
                return [a["title"] + " " + (a.get("description") or "") for a in articles[:20]]
        except:
            pass
        return []
    
    def fallback_news(self, symbol):
        return [
            f"Market analysis for {symbol}: bullish sentiment",
            f"Technical indicators show {symbol} in uptrend",
            f"Institutional interest in {symbol} increasing"
        ]
    
    def analyze_news(self, news_texts, direction):
        buy_words = ["up", "rise", "bull", "growth", "positive", "strong", "upgrade", "buy"]
        sell_words = ["down", "fall", "bear", "decline", "negative", "weak", "downgrade", "sell"]
        score = 0
        for text in news_texts:
            text_lower = text.lower()
            if direction == "BUY":
                for word in buy_words:
                    if word in text_lower:
                        score += 1
                for word in sell_words:
                    if word in text_lower:
                        score -= 0.5
            else:
                for word in sell_words:
                    if word in text_lower:
                        score += 1
                for word in buy_words:
                    if word in text_lower:
                        score -= 0.5
        return score
    
    def record_prediction(self, prediction):
        pred_id = hashlib.md5(f"{prediction.get('symbol', '')}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        entry = {
            "id": pred_id,
            "symbol": prediction.get("symbol"),
            "action": prediction.get("action"),
            "confidence": prediction.get("confidence"),
            "chapter_breakdown": prediction.get("chapter_breakdown", []),
            "timestamp": datetime.now().isoformat(),
            "correct": None,
            "price_after": None,
            "news_score": None
        }
        self.history.append(entry)
        self.save_history()
        return pred_id
    
    def learn_from_outcome(self, pred_id, actual_price_change, target_price=0):
        pred = None
        for p in self.history:
            if p["id"] == pred_id:
                pred = p
                break
        if not pred:
            return {"error": "Prediction not found"}
        action = pred.get("action")
        if action == "BUY":
            correct = actual_price_change > 0
        elif action == "SELL":
            correct = actual_price_change < 0
        else:
            correct = abs(actual_price_change) < 1
        pred["correct"] = correct
        pred["price_after"] = actual_price_change
        chapter_scores = pred.get("chapter_breakdown", [])
        learning_rate = 0.05
        for chapter in chapter_scores:
            chapter_num = chapter.get("chapter", "").replace("Chapter ", "").zfill(2)
            chapter_key = f"chapter_{chapter_num}"
            verdict = chapter.get("verdict", "NEUTRAL")
            if verdict == "PRO":
                if correct:
                    self.weights[chapter_key] = self.weights.get(chapter_key, 1.0) + learning_rate
                else:
                    self.weights[chapter_key] = self.weights.get(chapter_key, 1.0) - learning_rate
            elif verdict == "CON":
                if not correct:
                    self.weights[chapter_key] = self.weights.get(chapter_key, 1.0) + learning_rate
                else:
                    self.weights[chapter_key] = self.weights.get(chapter_key, 1.0) - learning_rate
        for k in self.weights:
            self.weights[k] = max(0.3, min(2.0, self.weights[k]))
        self.save_weights()
        self.save_history()
        return {"status": "learned", "correct": correct, "weights": self.weights}
    
    def auto_learn_from_news(self, symbol, predicted_action):
        news = self.fetch_news(symbol)
        if not news:
            return {"status": "no news", "news_count": 0}
        news_score = self.analyze_news(news, predicted_action)
        return {
            "status": "analyzed",
            "news_count": len(news),
            "news_score": news_score,
            "sentiment": "positive" if news_score > 0 else "negative" if news_score < 0 else "neutral"
        }

    def get_weights(self):
        return self.weights