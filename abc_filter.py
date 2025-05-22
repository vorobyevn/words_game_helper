import re


class AbcFilter:
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    filtered_abc = []
    mask = ""

    def __init__(self, world_len):
        self.world_len = world_len
        self.mask = "*" * self.world_len
        self.filtered_abc = set(self.alphabet)
        # self.exists = "*" * self.world_len
        self.exclude_positions = []
        for i in range(self.world_len):
            self.exclude_positions.append(set())

    def to_str(self):
        return "известные %s, доступные %s" % (self.mask, self.filtered_abc)

    def add_exists(self, mask):
        if len(mask) < self.world_len:
            mask = mask + ("*" * self.world_len - len(mask))
        elif len(mask) > self.world_len:
            mask = mask[:5]
        # self.exists = mask
        for idx, c in enumerate(mask):
            if c != "*":
                self.exclude_positions[idx].add(c)

    def exclude(self, chars):
        self.filtered_abc = self.filtered_abc - set(chars)

    def set_positions(self, mask):
        if len(mask) < self.world_len:
            mask = mask + ("*" * self.world_len - len(mask))
        elif len(mask) > self.world_len:
            mask = mask[:5]
        self.mask = mask

    def find_matched_words(self, words):
        filtered = []
        word_incl_re = self.generate_incl_regex()
        print(word_incl_re)
        word_excl_re = self.generate_excl_regex()
        print(word_excl_re)
        all_excluded = self.get_all_excluded()
        for w in words:
            matched = word_incl_re.match(w)
            if not matched:
                continue
            matched = word_excl_re.match(w)
            if not matched:
                continue
            if len(all_excluded - set(w)) > 0:
                continue
            filtered.append(w)
        return filtered

    def generate_incl_regex(self):
        pattern = ""
        for i in range(self.world_len):
            # if len(self.mask) > 0 and i < len(self.mask):
            if self.mask[i] == '*':
                pattern += self.get_incl_pattern(self.filtered_abc - set(self.exclude_positions[i]))
            else:
                pattern += self.mask[i]
        return re.compile(pattern)

    def generate_excl_regex(self):
        pattern = ""
        for i in range(self.world_len):
            if len(self.exclude_positions[i]) > 0:
                pattern += self.get_excl_pattern(self.exclude_positions[i])
            else:
                pattern += self.get_incl_pattern(self.filtered_abc)
        return re.compile(pattern)

    def get_incl_pattern(self, charset):
        return '[' + ''.join(charset) + ']'

    def get_excl_pattern(self, charset):
        return '[^' + ''.join(charset) + ']'

    def get_all_excluded(self):
        all = set()
        for s in self.exclude_positions:
            all = all.union(s)
        return all