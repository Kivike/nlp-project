from nltk.corpus import wordnet
import nltk
import numpy as np

nltk.download('wordnet')

class SentimentExtractor:
    synon_cache = {}
    stemmer = None

    def __init__(self):
        self.stemmer = nltk.PorterStemmer()

    def extract_feature(self, review: dict, words: list, sentiment: -1):
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

        all_synonyms = []
        all_antonyms = []
        
        for word in words:
            synonyms, antonyms = self.get_synonyms(word)

            synonyms = [self.stemmer.stem(s) for s in synonyms]
            antonyms = [self.stemmer.stem(a) for a in antonyms]

            all_synonyms.extend([s for s in synonyms if s not in all_synonyms])
            all_antonyms.extend([a for a in antonyms if a not in all_antonyms])

        content = review['Review Content']

        if isinstance(content, str):
            content = self.preprocess(content)

            for synonym in all_synonyms:
                if 'not ' + synonym in content:
                    value -= sentiment
                elif synonym in content:
                    value += sentiment

            for antonym in all_antonyms:
                if 'not ' + antonym in content:
                    value += sentiment
                elif antonym in content:
                    value -= sentiment

        return value

    def preprocess(self, content: str):
        return content.lower()

    def get_synonyms(self, word: str):
        if word in self.synon_cache:
            synonyms = self.synon_cache[word]['synonyms']
            antonyms = self.synon_cache[word]['antonyms']
        else:
            self.synon_cache[word] = {}
            synonyms = []
            antonyms = []

            for synset in wordnet.synsets(word):
                for lemma in synset.lemmas():
                    if lemma.name() not in synonyms:
                        synonyms.append(lemma.name())

                        for antonym in lemma.antonyms():
                            if antonym.name() not in antonyms:
                                antonyms.append(antonym.name())

            self.synon_cache[word]['synonyms'] = synonyms
            self.synon_cache[word]['antonyms'] = antonyms

            #if len(synonyms):
            #    print('Synonyms for %s: %s' % (word, synonyms))

            #if len(antonyms):
            #    print('Antonyms for %s: %s' % (word, antonyms))

        return synonyms, antonyms
        