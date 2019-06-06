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
        if speaker != None:
            print(speaker)
        if type(word_set_1) == str:
            word_set_1 = [word_set_1]
        if type(word_set_2) == str:
            word_set_2 = [word_set_2]
        occurences_A = [self.count_occurences(word_set_1, scenes_A, speaker), self.count_occurences(word_set_2, scenes_A, speaker)]
        occurences_B = [self.count_occurences(word_set_1, scenes_B, speaker), self.count_occurences(word_set_2, scenes_B, speaker)]
        if occurences_A[0] == 0 or occurences_A[1] == 0:
            occurence_ratio_A = 0
        else:
            occurence_ratio_A = occurences_A[0]/occurences_A[1]
        if occurences_B[0] == 0 or occurences_B[1] == 0:
            occurence_ratio_B = 0
        else:
            occurence_ratio_B = occurences_B[0]/occurences_B[1]
        percent_A = [self.percent_occurence(word_set_1, scenes_A, speaker), self.percent_occurence(word_set_2, scenes_A, speaker)]
        percent_B = [self.percent_occurence(word_set_1, scenes_B, speaker), self.percent_occurence(word_set_2, scenes_B, speaker)]
        if percent_A[0] == 0 or percent_A[1] == 0:
            ratio_A = 0
        else:
            ratio_A = percent_A[0]/percent_A[1]
        if percent_B[0] == 0 or percent_B[1] == 0:
            ratio_B = 0
        else:
            ratio_B = percent_B[0]/percent_B[1]
        # print(ratio_A, ratio_B)
        print("\t{}\t%\t{}\t%\tratio".format(word_set_1[0], word_set_2[0]))
        print("Part A\t{0:d}\t{1:.3f}\t{2:d}\t{3:.3f}\t{4:.3f}".format(occurences_A[0], percent_A[0]*100, occurences_A[1], percent_A[1]*100, ratio_A))
        print("Part B\t{0:d}\t{1:.3f}\t{2:d}\t{3:.3f}\t{4:.3f}".format(occurences_B[0], percent_B[0]*100, occurences_B[1], percent_B[1]*100, ratio_B))

    def compare_word(self, word_set, scenes_A, scenes_B, speaker=None):
        if type(word_set) == str:
            word_set = [word_set]
        occurences_A = self.count_occurences(word_set, scenes_A, speaker)
        occurences_B = self.count_occurences(word_set, scenes_B, speaker)
        percent_A = self.percent_occurence(word_set, scenes_A, speaker)
        percent_B = self.percent_occurence(word_set, scenes_B, speaker)
        if occurences_A == 0 or occurences_B == 0:
            occurence_ratio = 0
        else:
            occurence_ratio = occurences_A/occurences_B
        if percent_A == 0 or percent_B == 0:
            ratio = 0
        else:
            ratio = percent_A/percent_B
        print("\t{}\t%".format(word_set[0]))
        print("Part A\t{0}\t{1:.3f}".format(occurences_A, percent_A*100))
        print("Part B\t{0}\t{1:.3f}".format(occurences_B, percent_B*100))

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
                print("{}\tOnly Part B!".format(word))
                continue
            if b == 0:
                print("{}\tOnly Part A!".format(word))
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
        # Cleanup
        for part in best_partition:
            for act in self.play.acts:
                if part[act] == []:
                    del part[act]
        return best_ratio, best_partition

    def counter_part(self, part_a):
        part_b = {}
        for act in self.play.acts:
            for scene in self.play.acts[act]:
                if not scene in part_a.get(act, []):
                    if not act in part_b:
                        part_b[act] = []
                    part_b[act].append(scene)
        return part_b

if __name__ == '__main__':
    play = Play('titus.txt')
    analyzer = Analyzer(play)

    part_a = {1: [1], 2: [1,2], 4: [1]}
    part_b = {2: [3,4], 3: [1,2], 4: [2,3,4], 5: [1,2,3]}

    # broth = ['brother', 'brothers']
    broth = ['brothers']
    breth = ['brethen', 'bretheren', 'brethren']
    honour = ['honour', 'noble']
    dead = ['death', 'blood', 'death']
    queen = ['queen']
    empress = ['empress']
    hands = ['hand', 'hands']
    friend = ['friend', 'friends']
    rome = ['rome', 'roman', 'romans', 'romes']
    sweet = ['sweet', 'sweets']
    sons = ['son', 'sons', 'child', 'children', 'babe']
    father = ['father']

    # print(play.play[0][0]['words'])

    print("Number of uses of {}: {}".format(broth, analyzer.count_occurences(broth)))

    print("Uses of {}: {}".format('bretheren', analyzer.show_occurences('bretheren')))
    print("Uses of {}: {}".format('brethren', analyzer.show_occurences('brethren')))
    print("Uses of {}: {}".format('brethen', analyzer.show_occurences('brethen')))
    print("Uses of {}: {}\n".format(breth, analyzer.show_occurences(breth)))

    print("Most used words: {}\n".format(analyzer.sort(analyzer.filter(25), 60)))

    # print("Uses of {}: {}".format(hands, analyzer.show_occurences(hands)))
    print("Part A: {}\nPart B: {}\n".format(part_a, part_b))
    analyzer.compare_word(friend, part_a, part_b)
    analyzer.compare_word(hands, part_a, part_b)

    ratio, partition = analyzer.partition(hands)
    print("\nBest partition for hands (with ratio {}): \n\tPart A {}\n\tPart B {}\n".format(ratio, partition[0], partition[1]))


    print("\nMost used words by {}: {}".format('TITUS', analyzer.sort(analyzer.filter(14, speaker='TITUS'), 45)))
    print("\nMost used words by {}: {}".format('SATURNINUS', analyzer.sort(analyzer.filter(10, speaker='SATURNINUS'), 45)))
    print("\nMost used words by {}: {}".format('TAMORA', analyzer.sort(analyzer.filter(10, speaker='TAMORA'), 45)))
    print("\nMost used words by {}: {}".format('LUCIUS', analyzer.sort(analyzer.filter(10, speaker='LUCIUS'), 45)))

    print("\nTITUS usage of 'Rome' (and variations):")
    analyzer.compare_word(rome, part_a, part_b, speaker='TITUS')
    print("\nSATURNINUS usage of 'Rome' (and variations):")
    analyzer.compare_word(rome, part_a, part_b, speaker='SATURNINUS')
    print("\nLUCIUS usage of 'Rome' (and variations):")
    analyzer.compare_word(rome, part_a, part_b, speaker='LUCIUS')
    print("\nTAMORA usage of 'Rome' (and variations):")
    analyzer.compare_word(rome, part_a, part_b, speaker='TAMORA')
    print("\nMARCUS usage of 'Rome' (and variations):")
    analyzer.compare_word(rome, part_a, part_b, speaker='MARCUS')
    analyzer.compare_word(rome, part_a, part_b)

    # print("\nMARCUS usage of 'Rome' (and variations):")
    # analyzer.compare_word(father, part_a, part_b, speaker='LUCIUS')
    # print("\nTAMORA usage of 'sons' (and variations):")
    analyzer.compare_word(sons, part_a, part_b, speaker='TAMORA')
    print("\nTAMORA usage of 'sweet' (and variations):")
    analyzer.compare_word(sweet, part_a, part_b, speaker='TAMORA')

    print("\nSynonym word comparisons:")
    analyzer.compare_words(broth, breth, part_a, part_b)
    analyzer.compare_words(queen, empress, part_a, part_b)
    analyzer.compare_words(honour, dead, part_a, part_b)

    analyzer.compare_word(['brother', 'brothers'], part_a, part_b)

    for speaker in play.speaker_words:
        if any([word in play.speaker_words[speaker] for word in queen]) or any([word in play.speaker_words[speaker] for word in empress]):
            analyzer.compare_words(queen, empress, part_a, part_b, speaker=speaker)
    
    analyzer.compare_words('king', 'emperor', part_a, part_b)


interesting = ['honour', 'friends', 'moor', ('queen', 'empress'), 'blood', 'hands', 'death', 'love', 'noble']