from jamie import Play, nonwords
import copy

class Analyzer:
    def __init__(self, play):
        self.play = play

    def filter(self, min_uses, scenes=None, speaker=None):
        if scenes == None:
            scenes = self.play.acts

        if speaker == None:
            play_words = self.play.words
        else:
            play_words = self.play.speaker_words[speaker]

        new_set = {}
        for word in play_words:
            if word in nonwords:
                continue
            num_uses = 0
            for act in scenes:
                if not act in play_words[word]:
                    continue
                for scene in scenes[act]:
                    if not scene in play_words[word][act]:
                        continue
                    num_uses += play_words[word][act][scene]
                    if num_uses >= min_uses:
                        new_set[word] = num_uses
        return new_set

    def compare_words(self, word_set_1, word_set_2, scenes_A, scenes_B, speaker=None):
        if type(word_set_1) == str:
            word_set_1 = [word_set_1]
        if type(word_set_2) == str:
            word_set_2 = [word_set_2]
        occurences_A = [self.count_occurences(word_set_1, scenes_A, speaker), self.count_occurences(word_set_2, scenes_A, speaker)]
        occurences_B = [self.count_occurences(word_set_1, scenes_B, speaker), self.count_occurences(word_set_2, scenes_B, speaker)]
        ratio_A = occurences_A[0]/occurences_A[1]
        ratio_B = occurences_B[0]/occurences_B[1]
        # print(ratio_A, ratio_B)
        print("\t{}\t{}".format(word_set_1[0], word_set_2[0]))
        print("A\t{}\t{}".format(occurences_A[0], occurences_A[1]))
        print("B\t{}\t{}".format(occurences_B[0], occurences_B[1]))

    def compare_word(self, word_set, scenes_A, scenes_B, speaker=None):
        if type(word_set) == str:
            word_set = [word_set]
        occurences_A = self.count_occurences(word_set, scenes_A, speaker)
        occurences_B = self.count_occurences(word_set, scenes_B, speaker)
        ration = occurences_A/occurences_B
        print("\t{}".format(word_set[0]))
        print("A\t{}".format(occurences_A))
        print("B\t{}".format(occurences_B))

    def count_occurences(self, word_set, scenes=None, speaker=None):
        if type(word_set) == str:
            word_set = [word_set]

        if scenes == None:
            scenes = self.play.acts

        if speaker == None:
            play_words = self.play.words
        else:
            play_words = self.play.speaker_words[speaker]

        occurences = 0
        for act in scenes:
            for scene in scenes[act]:
                for word in word_set:
                    if not word in play_words:
                        continue
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
            play_words = self.play.words
        else:
            play_words = self.play.speaker_words[speaker]

        occurences = {}
        for act in scenes:
            occurences[act] = {}
            for scene in scenes[act]:
                occurences[act][scene] = 0
                for word in word_set:
                    if not word in play_words:
                        continue
                    if not act in play_words[word]:
                        continue
                    if not scene in play_words[word][act]:
                        continue
                    occurences[act][scene] = play_words[word][act][scene] + occurences[act].get(scene, 0)
        return occurences

    def percent_occurence(self, word_set, scenes=None, speaker=None):
        if type(word_set) == str:
            word_set = [word_set]

        if scenes == None:
            scenes = self.play.acts

        if speaker == None:
            play_words = self.play.words
        else:
            play_words = self.play.speaker_words[speaker]

        if speaker == None:
            play_lengths = self.play.lengths
        else:
            play_lengths = self.play.speaker_lengths[speaker]


        num_occurences = self.count_occurences(word_set, scenes, speaker)
        total_length = 0
        for act in scenes:
            if not act in play_lengths:
                continue
            for scene in scenes[act]:
                if not scene in play_lengths[act]:
                    continue
                total_length += play_lengths[act][scene]
        if total_length == 0:
            return 0
        return num_occurences/total_length

    def sort(self, words, n=None):
        if n == None:
            n = len(words)
        return {word: words[word] for word in sorted(words, key=words.get, reverse=True)[:n]}

    def compare_many_words(self, words, scenes_a, scenes_b):
        for word in words:
            self.compare_word(word, scenes_a, scenes_b)
            a = self.percent_occurence(word, scenes=scenes_a)
            b = self.percent_occurence(word, scenes=scenes_b)
            if a == 0:
                print("{}\tOnly part B!".format(word))
                continue
            if b == 0:
                print("{}\tOnly part A!".format(word))
                continue
            ratio = a/b
            thresh = 2
            if ratio < 1:
                if 1/ratio > thresh:
                    print("{}\tb>a\t{}".format(word, 1/ratio))
            else:
                if ratio > thresh:
                    print("{}\ta>b\t{}".format(word, ratio))

    def partition(self, word_set, speaker=None): # does not include 0's

        part_a = {act: [] for act in self.play.acts}
        part_b = {act: [scene for scene in self.play.acts[act]] for act in self.play.acts}

        def get_ratio(part_a, part_b):
            a = self.percent_occurence(word_set, scenes=part_a, speaker=speaker)
            b = self.percent_occurence(word_set, scenes=part_b, speaker=speaker)
            if a == 0 or b == 0:
                return 0
            elif a > b:
                return a/b
            else:
                return b/a

        best_partition = copy.deepcopy((part_a, part_b))
        best_ratio = get_ratio(part_a, part_b)

        for act in self.play.acts:
            for scene in self.play.acts[act]:
                part_a[act].append(scene)
                part_b[act].remove(scene)
                # print(part_a, part_b)
                ratio = get_ratio(part_a, part_b)
                # print(ratio)
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_partition = copy.deepcopy((part_a, part_b))

        return best_ratio, best_partition


if __name__ == '__main__':
    play = Play('titus.txt')
    analyzer = Analyzer(play)
    broth = ['brother', 'brothers']
    breth = ['bretheren', 'brethren', 'brethen']
    honour = ['honour', 'noble']
    dead = ['death', 'blood', 'death']
    queen = ['queen']
    empress = ['empress']
    hands = ['hand', 'hands']
    part_a = {0: [0], 1: [0,1], 3: [0]}
    part_b = {1: [2,3], 2: [0,1], 3: [1,2,3], 4: [0,1,2]}
    # for act in play.acts:
    #     part_b[act] = []
    #     for scene in play.acts[act]:
    #         if not scene in part_a.get(act, []):
    #             part_b[act].append(scene)
    # print(part_b)

    # print(analyzer.count_occurences(['brother', 'brothers']))
    # analyzer.compare_words(broth, breth, part_a, part_b)
    # analyzer.compare_words(queen, empress, part_a, part_b)
    # analyzer.compare_words(honour, dead, part_a, part_b)
    # analyzer.compare_word(['friend', 'friends'], part_a, part_b)
    # print(play.play[0][0]['words'])
    # words = analyzer.filter(14, speaker='TITUS')
    # print(analyzer.sort(words))#, 10))

    # print(analyzer.show_occurences(broth))
    print(analyzer.show_occurences(hands))
    analyzer.compare_word(hands, part_a, part_b)
    print(analyzer.partition(hands))
    # print(analyzer.show_occurences('bretheren'))
    # print(analyzer.show_occurences('brethren'))
    # print(analyzer.show_occurences('brethen'))


interesting = ['honour', 'friends', 'moor', ('queen', 'empress'), 'blood', 'hands', 'death', 'love', 'noble']