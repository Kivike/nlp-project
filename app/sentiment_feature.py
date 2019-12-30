

class SentimentFeature:

    name = ''
    words = []
    sentiment = 1

    def __init__(self, name: str, words: list, sentiment: int):
        """
        Keyword arguments:

        name -- Name of feature, used as column name
        words -- Words to look for in content string
        sentiment -- +1 if words mean a positive thing, -1 if negative
        """
        self.name = name
        self.words = words
        self.sentiment = sentiment