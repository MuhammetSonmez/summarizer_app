import networkx as nx
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TextSummarizer:
    def __init__(self, text, num_sentences=1):
        self.text = text
        self.num_sentences = num_sentences
        self.sentences = sent_tokenize(text)
        self.sentence_vectors = self._generate_sentence_vectors()
        self.similarity_matrix = self._calculate_similarity_matrix()
        self.graph = self._build_graph()
        self.scores = nx.pagerank(self.graph)

    def _generate_sentence_vectors(self):
        vectorizer = TfidfVectorizer()
        return vectorizer.fit_transform(self.sentences).toarray()

    def _calculate_similarity_matrix(self):
        return cosine_similarity(self.sentence_vectors)

    def _build_graph(self):
        return nx.from_numpy_array(self.similarity_matrix)

    def summarize(self):
        ranked_sentences = sorted(((self.scores[i], s) for i, s in enumerate(self.sentences)), reverse=True)
        summary = " ".join([ranked_sentences[i][1] for i in range(min(self.num_sentences, len(ranked_sentences)))])
        return summary
