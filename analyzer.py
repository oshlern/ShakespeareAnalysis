from jamie import Play, nonwords

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

    def compare_words(self, word_set_1, word_set_2, scenes_A, scenes_B, speaker=None):
        occurences_A = [self.count_occurences(word_set_1, scenes_A, speaker), self.count_occurences(word_set_2, scenes_A, speaker)]
        occurences_B = [self.count_occurences(word_set_1, scenes_B, speaker), self.count_occurences(word_set_2, scenes_B, speaker)]
        ratio_A = occurences_A[0]/occurences_A[1]
        ratio_B = occurences_B[0]/occurences_B[1]
        print(ratio_A, ratio_B)
        # for act in play.play:
        #     for scene in play.play[act]:

    def count_occurences(self, word_set, scenes=None, speaker=None):
        if type(word_set) == str:
            word_set = [word_set]

        if scenes == None:
            scenes = play.acts

        if speaker == None:
            play_words = play.words
        else:
            play_words = play.speaker_words[speaker]

        occurences = 0
        for act in scenes:
            for scene in scenes[act]:
                for word in word_set:
                    if not act in play_words[word]:
                        continue
                    if not scene in play_words[word][act]:
                        continue
                    occurences += play_words[word][act][scene]
        return occurences

    def show_occurences(self, word_set, speaker=None):
        if type(word_set) == str:
            word_set = [word_set]

        scenes = play.acts

        if speaker == None:
            play_words = play.words
        else:
            play_words = play.speaker_words[speaker]

        occurences = {}
        for act in scenes:
            occurences[act] = {}
            for scene in scenes[act]:
                occurences[act][scene] = 0
                for word in word_set:
                    if not act in play_words[word]:
                        continue
                    if not scene in play_words[word][act]:
                        continue
                    occurences[act][scene] = play_words[word][act][scene] + occurences[act].get(scene, 0)
        return occurences


if __name__ == '__main__':
    play = Play('titus.txt')
    analyzer = Analyzer(play)
    broth = ['brother', 'brothers']
    breth = ['bretheren', 'brethren', 'brethen']
    part_a = {0: [0], 1: [0,1], 3: [0]}
    part_b = {1: [2,3], 2: [0,1], 3: [1,2,3], 4: [0,1,2]}
    # for act in play.acts:
    #     part_b[act] = []
    #     for scene in play.acts[act]:
    #         if not scene in part_a.get(act, []):
    #             part_b[act].append(scene)
    # print(part_b)

    # print(analyzer.count_occurences(['brother', 'brothers']))
    print(analyzer.compare_words(broth, breth, part_a, part_b))
    # print(play.play[0][0]['words'])
    # print(analyzer.filter(play.play[0][0]['words'], 15, 5))
    print(play.words)
    print(analyzer.filter(play.words, 15, 5))
    # print(analyzer.show_occurences(broth))
    # print(analyzer.show_occurences(breth))
    # print(analyzer.show_occurences('bretheren'))
    # print(analyzer.show_occurences('brethren'))
    # print(analyzer.show_occurences('brethen'))