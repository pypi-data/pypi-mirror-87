from gensim.models.phrases import Phraser as GSPhraser
from gensim.models import word2vec, KeyedVectors
from gensim.models.phrases import Phrases
import joblib
import json

from texta_tools.text_processor import TextProcessor
from . import exceptions


class Phraser:

    def __init__(self):
        self._phraser = None 
    

    def train(self, sentences):
        phrase_model = Phrases(sentences)
        phraser = GSPhraser(phrase_model)
        self._phraser = phraser


    def phrase(self, text):
        if self._phraser:
            if isinstance(text, str):
                text = text.split(' ')
                return ' '.join(self._phraser[text])
            else:
                return self._phraser[text]
        else:
            return text



class W2VEmbedding:

    def __init__(self, description=None, workers=1, min_freq=5, num_dimensions=100, 
                 text_processor=TextProcessor(sentences=True, remove_stop_words=True, words_as_list=True)):
        self.model = None
        self.phraser = None
        self.description = description
        # params
        self.workers = workers
        self.min_freq = min_freq
        self.num_dimensions = num_dimensions
        self.text_processor = text_processor


    def train(self, texts, use_phraser=True):
        """
        Trains Word2Vec embedding.
        :param: list texts: List of texts or an iterator (e.g. Elasticsearcher).
        """
        if not texts:
            raise exceptions.InvalidInputError("No training texts provided.")
        # add texts to text processor so we can use it as an iterator
        self.text_processor.input_texts = texts
        # build phraser if asked
        if use_phraser == True:
            phraser = Phraser()
            phraser.train(self.text_processor)
            # set phraser
            self.phraser = phraser
            # update phraser in text processor
            self.text_processor.phraser = phraser
        # word2vec model
        num_passes = 5
        total_passes = num_passes + 1
        model = word2vec.Word2Vec(
            self.text_processor,
            min_count=self.min_freq,
            size=self.num_dimensions,
            iter=int(num_passes),
            workers=self.workers
        )
        self.model = model
        return True


    def save(self, file_path):
        to_dump = {"phraser": self.phraser, "embedding": self.model}
        joblib.dump(to_dump, file_path)
        return True


    def load(self, file_path):
        to_load = joblib.load(file_path)
        self.model = to_load["embedding"]
        self.phraser = to_load["phraser"]
        return True


    def load_django(self, embedding_object):
        """
        Loads embedding Django.
        """
        file_path = embedding_object.embedding_model.path
        to_load = joblib.load(file_path)
        self.model = to_load["embedding"]
        self.phraser = to_load["phraser"]
        self.name = embedding_object.description
        return True


    def get_similar(self, positives, negatives=[], n=20):
        """
        Find similar words & phraser for input list of strings.
        """
        for input_list in (positives, negatives):
            if not isinstance(input_list, list):
                raise exceptions.InvalidInputError("Input must be list!")
        positives = [positive.replace(' ', '_') for positive in positives]
        negatives = [negative.replace(' ', '_') for negative in negatives]
        # filter out words not present in the embedding vocabulary
        positives = [positive for positive in positives if positive in self.model.wv.vocab]
        negatives = [negative for negative in negatives if negative in self.model.wv.vocab]
        if positives:
            similar_items = self.model.wv.most_similar(positive=positives, negative=negatives, topn=n)
            similar_items = [{'phrase': s[0].replace('_', ' '), 'score': s[1], 'model': self.name} for s in similar_items if s[0] not in negatives]
            return similar_items
        else:
            return []


    def get_vector(self, word):
        """
        Returns vector for given embedding entry.
        """
        if word not in self.model.wv.index2word:
            raise exceptions.OutOfVocabError("Word or phrase not in vocabulary.")
        return self.model.wv.__getitem__(word)


    def get_vocabulary(self):
        """
        Returns embedding vocabulary from KeyedVectors.
        """
        return self.model.wv.index2word
