
class FeatureExtractor:

    def extract_features(self, review: dict):
        value = 0

        # TODO Get synonyms with wordnet?
        unsafe_synonyms = [
            "unsafe",
            "not safe",
            "risky",
            "untrustworthy",
            "alarming",
            "unreliable",
            "treacherous",
            "risky",
            "perilous"
        ]

        stars = review['Review Stars']

        if stars <= 2:
            content = review['Review Content']

            for word in unsafe_synonyms:
                if word in content:
                    value += 1

        return value
