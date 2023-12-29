class ExactMatchBot:
    def __init__(self, corpus, match_corpus=None):
        if match_corpus is None:
            match_corpus = []
        self.corpus = corpus
        if len(match_corpus) == 0:
            self.match_corpus = corpus
        else:
            self.match_corpus = match_corpus

    def search(self, query):
        results = set()
        for i in range(len(self.corpus)):
            sentence = self.corpus[i]
            for word in query:
                if word in sentence:
                    results.add(self.match_corpus[i][0])
                    continue
        return results

