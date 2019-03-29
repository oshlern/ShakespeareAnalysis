from jamie import Play, Markov, nonwords

class Analyzer:
    def __init__(self, play):
        self.play = play

    def filter(self, word_set, min_uses, min_afters=1):
        # word_set.remove('~last')
        new_set = {}
        for word in word_set:
            if word in nonwords:
                continue
            num_uses = 0
            for prev_word in word_set[word]:
                # print(word, word_set[word])
                num_uses += word_set[word][prev_word]
            if num_uses >= min_uses:
                new_set[word] = {}
                for prev_word in word_set[word]:
                    if word_set[word][prev_word] >= min_afters:
                        new_set[word][prev_word] = word_set[word][prev_word]
        return new_set

    # def diff(word_set1, word_set2):

if __name__ == '__main__':
    play = Play('titus.txt')
    analyzer = Analyzer(play)
    # print(play.play[0][0]['words'])
    # print(analyzer.filter(play.play[0][0]['words'], 15, 5))