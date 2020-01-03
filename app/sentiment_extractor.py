from nltk.corpus import wordnet
import nltk
from nltk.tokenize import word_tokenize
import numpy as np

nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')

class SentimentExtractor:
    synon_cache = {}
    stemmer = None

    def __init__(self):
        self.stemmer = nltk.PorterStemmer()

    def extract_feature(self, review: dict, words: list, sentiment: -1) -> float:
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

            for s in synonyms:
                if s not in all_synonyms:
                    all_synonyms.append(s)
                    all_antonyms.append('not ' + s)

            for a in antonyms:
                if a not in all_antonyms:
                    all_antonyms.append(a)
                    all_synonyms.append('not ' + a)

        content = review['Review Content']

        if isinstance(content, str):
            words = self.get_relevant_words(content)

            for word in words:
                for synonym in all_synonyms:
                    if word.startswith(synonym):
                        value += sentiment
                        break
                else:
                    for antonym in all_antonyms:
                        if word.startswith(antonym):
                            value -= sentiment
                            break

            return value / len(words)
        else:
            return 0

    def get_relevant_words(self, content: str) -> List[str]:
        """
        Get list of relevant words in the review content
        Only keeps nouns, adjectives, and verbs
        """
        tokenized = word_tokenize(content.lower())
        pos_words = nltk.pos_tag(tokenized)

        relevant_words = []

        for i in range(0, len(pos_words)):
            word, pos_tag = pos_words[i]

            if pos_tag.startswith(('NN', 'JJ', 'VB')):
                # Add 'not' from previous word to the word it is referring to
                if i > 0 and pos_words[i - 1][0] == 'not':
                    word = 'not ' + word

                relevant_words.append(word)

        return relevant_words

    def get_synonyms(self, word: str):
        """
        Get synonyms and antonyms of a word from WordNet
        """
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
        