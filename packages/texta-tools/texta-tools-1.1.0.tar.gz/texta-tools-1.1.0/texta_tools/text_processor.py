import os


class StopWords:
    """
    Stop word remover using existing lists.
    """
    def __init__(self, custom_stop_words=[]):
        self.stop_words = self._get_stop_words(custom_stop_words)
    
    @staticmethod
    def _get_stop_words(custom_stop_words):
        stop_words = {}
        stop_word_dir = os.path.join(os.path.dirname(__file__), 'stop_words')
        for f in os.listdir(stop_word_dir):
            with open('{0}/{1}'.format(stop_word_dir, f), encoding="utf8") as fh:
                for stop_word in fh.read().strip().split('\n'):
                    stop_words[stop_word] = True

        for custom_stop_word in custom_stop_words:
            stop_words[custom_stop_word] = True     

        return stop_words

    def remove(self, text):
        if isinstance(text, str):
            return ' '.join([lemma for lemma in text.split(' ') if lemma not in self.stop_words])
        elif isinstance(text, list):
            return [lemma for lemma in text if lemma not in self.stop_words]
        else:
            return None


class TextProcessor:
    """
    Processor for processing texts prior to modelling
    """

    def __init__(self, lemmatizer=None, phraser=None, tokenizer=None, remove_stop_words=True, sentences=False, 
                 words_as_list=False, custom_stop_words=[], input_texts=None):
        # processing resources
        self.lemmatizer = lemmatizer
        self.phraser = phraser
        self.tokenizer = tokenizer
        self.stop_words = StopWords(custom_stop_words=custom_stop_words)
        # processing options
        self.remove_stop_words = remove_stop_words
        self.sentences = sentences
        self.words_as_list = words_as_list
        # this is for when processor is used as an iterator (e.g. for gensim training)
        self.input_texts = input_texts


    def __iter__(self):
        if self.input_texts:
            for input_text in self.input_texts:
                processed = self.process(input_text)
                if processed:
                    yield processed[0]


    def _tokenize_and_lemmatize(self, text):
        """
        Tokenizes and lemmatizes text using MLP if asked.
        :param: str text: Input text to be tokenized & lemmatized.
        :return: Tokenized & lemmatized text.
        """
        # MLP lemmatizer tokenizes text anyway, so we don't need to do it again
        if self.lemmatizer:
            return self.lemmatizer.lemmatize(text)
        # tokenize without lemmatizing
        if self.tokenizer:
            return self.tokenizer.process(text)["text"]["text"]
        # return input text if nothing done
        return text


    def process(self, input_text):
        if isinstance(input_text, str):
            stripped_text = input_text.strip()
            if self.sentences:
                list_of_texts = stripped_text.split('\n')
            else:
                list_of_texts = [stripped_text]
        else:
            # whetever obscure was found, output is as string
            list_of_texts = [str(input_text)]
        out = []
        for text in list_of_texts:
            if text:
                # make sure it is a string
                text = str(text)
                # tokenize & lemmatize if asked
                text = self._tokenize_and_lemmatize(text)
                # lower & strip
                text = text.lower().strip()
                # convert string to list of tokens
                tokens = text.split(' ')
                # remove stop words
                if self.remove_stop_words:
                    tokens = self.stop_words.remove(tokens)
                # use phraser
                if self.phraser:
                    tokens = self.phraser.phrase(tokens)
                # remove empty tokens
                tokens = [token for token in tokens if token]
                # prepare output
                if not self.words_as_list:
                    out.append(' '.join([token.replace(' ', '_') for token in tokens]))
                else:
                    out.append(tokens)
        # return list of strings
        if self.sentences or self.words_as_list:
            return out
        # return first value as string
        elif out:
            return out[0]
        else:
            return ""
