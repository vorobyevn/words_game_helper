import codecs
import random


class NounsDict():
    nouns_file = 'words52.txt'
    start_words_chars_limit = 7
    nouns = []
    chars_frequency = []
    # word_freq = None
    abc_freq = None

    def __init__(self):
        self.nouns = self.load_nouns()
        self.nouns = self.get_filtered_nouns()

    def load_nouns(self):
        with codecs.open(self.nouns_file, encoding="UTF8") as f:
            nouns = f.readlines()
            nouns = list(map(str.strip, nouns))
        return nouns

    def get_nouns(self):
        return self.nouns

    def get_chars_frequency(self):
        if not self.chars_frequency:
            frequency = self.get_chars_frequency_list()
            self.chars_frequency = sorted(frequency, key=lambda x: x[1], reverse=True)
        return self.chars_frequency

    def get_filtered_nouns(self, worlds_len=5):
        return [n for n in self.nouns if len(n) == worlds_len]

    def most_frequent_chars(self, limit):
        freq = self.get_chars_frequency()[:limit]
        return [c[0] for c in freq]

    def get_chars_frequency_list(self):
        abc_freq = self.get_abc_freq_dict()
        freq = list(abc_freq.items())
        return freq

    def get_abc_freq_dict(self):
        total = 0
        if not self.abc_freq:
            self.abc_freq = {}
            for word in self.get_nouns():
                for c in word:
                    total += 1
                    if c in self.abc_freq:
                        self.abc_freq[c][0] = self.abc_freq[c][0] + 1
                    else:
                        self.abc_freq[c] = [1, 1]
            for item in self.abc_freq.values():
                if total > 0:
                    item[1] = item[1] / total
        return self.abc_freq

    def find_start_words(self, limit=7):
        char_arr = self.most_frequent_chars(limit)
        chars_set = set(char_arr)
        words_from_frequent_chars = []
        for w in self.nouns:
            word_set = set(w)
            if len(word_set) < len(w):
                # буквы в слове повторяются
                continue
            excluded_chars = word_set - chars_set
            if excluded_chars:
                # есть буквы в слове не из самых частых букв
                continue
            words_from_frequent_chars.append(w)
        return words_from_frequent_chars

    def find_rnd_start_word(self, limit=None):
        if not limit:
            limit = self.start_words_chars_limit
        words = self.find_start_words(limit)
        return random.choice(words)

    def sort_by_frequency(self, words, limit=50):
        # if not self.word_freq:
        abc_freq = self.get_abc_freq_dict()
        words_freq = []
        for idx, w in enumerate(words):
            word_freq = 0
            for c in set(w):
                if c in abc_freq:
                    word_freq += abc_freq[c][1]
            words_freq.append((w, word_freq))
        sorted_words = sorted(words_freq, key=lambda x: x[1], reverse=True)[:limit]
        return [w[0] for w in sorted_words]
