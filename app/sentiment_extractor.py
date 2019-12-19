from nltk.corpus import wordnet
import nltk
import numpy as np

nltk.download('wordnet')

class SentimentExtractor:
    def extract_feature(self, review: dict, word: str, sentiment: -1):
        """
        Extract sentiment based on given word
        Also uses synonyms and antonyms of selected word

        Keyword arguments:

        review -- Review row from TripAdvisor data
        word -- Word to look for to calculate feature value
        sentiment -- -1 if given word is a negative one, 1 if positive one
            antonyms will be given the opposite value
        """
        value = 0
        synonyms, antonyms = self.get_synonyms(word)

        content = review['Review Content']

        if content is not np.nan:
            for synonym in synonyms:
                if 'not ' + synonym in content:
                    value -= sentiment
                elif synonym in content:
                    value += sentiment

            for antonym in antonyms:
                if 'not ' + antonym in content:
                    value += sentiment
                elif antonym in content:
                    value -= sentiment

        return value

    def get_synonyms(self, word: str):
        synonyms = []
        antonyms = []

        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name())

                    for antonym in lemma.antonyms():
                        if antonym.name() not in antonyms:
                            antonyms.append(antonym.name())

        return synonyms, antonyms
        