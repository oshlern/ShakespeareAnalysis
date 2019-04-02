import re, random, preprocess
# Markov Chain For Shakespeare Plays
# First Chain: Who is talking - {Othello: {2: Desdemona, 18: Desdemona, ...}, Iago.}

# Data sorted into markov subsequencies of words, line lengths, and speech lengths.
# Calculated by speaker and speaker-ambiguous, as well as scene-specific and play-wide.
# ~null: {1: Let}, Let: {1: him}, him: {...}
# speakers = {'~null': {}, 'Othello': {2: 'Iago', 18: 'Desdemona', ...}, 'Iago': {}}
# speeches = {'Othello': {'lines': {12: 1, 23: 2, 68: 3}, 'words': {'~null': {}, 'hi': {'.': 12, 'there'``}, '.':  }}}
# can Make more sophisticated: what words are said more after certain speakers, speech_lens, etc. or at which point in the speech or dialogue

nonwords = ['.', ',', ';', ':', '-', '!', '?', '_', '(', ')', '~last']

class Play:
    def __init__(self, doc):
        self.openDoc(doc)

        self.words = {}
        self.speaker_words = {}
        self.acts = {}
        self.lengths = {}
        self.speaker_lengths = {}

        self.parseText()

    def openDoc(self, doc):
        processed_file = "processed_" + doc
        preprocess.preprocess(doc, processed_file)
        processed = open(processed_file, 'r')
        self.text = processed.read()

    def update_occurences(self, item, superset):
        if not item in superset:
            superset[item] = {}
        superset[superset['~last']][item] = 1 + superset[superset['~last']].get(item, 0)
        superset['~last'] = item

    def parseText(self):
        acts = self.text.split('|act|')[1:]
        for act_num, act in enumerate(acts):
            self.words[act_num] = {}
            self.lengths[act_num] = {}
            self.acts[act_num] = []
            scenes = act.split('|scene|')[1:]
            for scene_num, scene in enumerate(scenes):
                self.words[act_num][scene_num] = {}
                self.lengths[act_num][scene_num] = 0
                self.acts[act_num].append(scene_num)
                speeches = scene.split('|speaker|')[1:]
                for speech in speeches:
                    speaker, lines = speech.split('|lines|')
                    lines = lines.split('\n')[:-1]

                    # Initialize speaker_words dict
                    if not speaker in self.speaker_words:
                        self.speaker_words[speaker] = {}
                    if not speaker in self.speaker_lengths:
                        self.speaker_lengths[speaker] = {}
                    if not act_num in self.speaker_lengths[speaker]:
                        self.speaker_lengths[speaker][act_num] = {}
                    if not scene_num in self.speaker_lengths[speaker][act_num]:
                        self.speaker_lengths[speaker][act_num][scene_num] = 0

                    for line in lines:
                        # chars = re.sub(r'([a-zA-z-\'])([^a-zA-z-\' ])', r'\1', line)
                        chars = re.sub(r'(\w+)\'\w*', r'\1', line)
                        chars = re.sub(r'\'(\w+?)\b', r'\1', chars)
                        chars = re.sub(r'([^\'])\b([^\'])', r'\1|word_break|\2', chars)
                        # chars = re.sub(r'\b', r'|word_break|', chars)
                        chars = re.sub(' ', '', chars)
                        chars = chars.lower()
                        words = chars.split('|word_break|')
                        for word in words:
                            # Could optimize if statements but chose not to for readability
                            for word_set in [self.words, self.speaker_words[speaker]]:
                                if not word in word_set:
                                    word_set[word] = {}
                                if not act_num in word_set[word]:
                                    word_set[word][act_num] = {}
                                if not scene_num in word_set[word][act_num]:
                                    word_set[word][act_num][scene_num] = 0
                                word_set[word][act_num][scene_num] += 1
                        self.lengths[act_num][scene_num] += len(words)
                        self.speaker_lengths[speaker][act_num][scene_num] += len(words)


    def saveData(self, doc, data):
        output = open(doc,"w")
        output.write(data)

if __name__ == '__main__':
    play = Play('titus.txt')
    print('brethren', play.words['brethren'])
    print('bretheren', play.words['bretheren'])
    print('brother', play.words['brother'])
    print('brothers', play.words['brothers'])