from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class sentiment_analyzer:
    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()
    def analyse_sentiment(self, sentence):
        sentiment = self.analyzer.polarity_scores(sentence)
        return sentiment
