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

        self.play = {}
        self.speakers = {'~null': {}, '~last': '~null'}
        self.words, self.line_lens, self.speech_lens = {'~null': {}, '~last': '~null'}, {'~null': {}, '~last': '~null'}, {'~null': {}, '~last': '~null'}
        self.speaker_words, self.speaker_line_lens, self.speaker_speech_lens = {}, {}, {}
        self.act_lengths, self.scene_lengths = [], []

        self.parseText()
        self.resetLasts()

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
            self.play[act_num] = {}
            scenes = act.split('|scene|')[1:]
            self.act_lengths.append(len(scenes))
            for scene_num, scene in enumerate(scenes):
                self.play[act_num][scene_num] = {'words': {'~null': {}, '~last': '~null'}, 'line_lens': {'~null': {}, '~last': '~null'}, 'speech_lens': {'~null': {}, '~last': '~null'},
                                                 'speaker_words': {}, 'speaker_line_lens': {}, 'speaker_speech_lens': {},
                                                 'speakers': {'~null': {}, '~last': '~null'}}
                speeches = scene.split('|speaker|')[1:]
                self.scene_lengths.append(len(speeches))
                for speech in speeches:
                    speaker, lines = speech.split('|lines|')
                    lines = lines.split('\n')[:-1]

                    # Initialize speaker
                    for superset in [self.speaker_words, self.speaker_line_lens, self.speaker_speech_lens,
                                     self.play[act_num][scene_num]['speaker_words'], self.play[act_num][scene_num]['speaker_line_lens'], self.play[act_num][scene_num]['speaker_speech_lens']]:
                        if not speaker in superset:
                            superset[speaker] = {'~null': {}, '~last': '~null'}
                    for superset in [self.speakers, self.play[act_num][scene_num]['speakers']]:
                        self.update_occurences(speaker, superset)

                    for line in lines:
                        chars = re.sub(r'([a-zA-z-\'])([^a-zA-z-\'])', r'\1', line)
                        chars = re.sub(r'([^\'])\b([^\'])', r'\1|word_break|\2', line)
                        chars = re.sub(' ', '', chars)
                        chars = chars.lower()
                        words = chars.split('|word_break|')
                        for word in words:
                            # Words
                            for superset in [self.words, self.play[act_num][scene_num]['words'],
                                             self.speaker_words[speaker], self.play[act_num][scene_num]['speaker_words'][speaker]]:
                                self.update_occurences(word, superset)
                        # Line lengths
                        for superset in [self.line_lens, self.play[act_num][scene_num]['line_lens'],
                                         self.speaker_line_lens[speaker], self.play[act_num][scene_num]['speaker_line_lens'][speaker]]:
                            self.update_occurences(len(words), superset)
                    # Speech lengths
                    for superset in [self.speech_lens, self.play[act_num][scene_num]['speech_lens'],
                                     self.speaker_speech_lens[speaker], self.play[act_num][scene_num]['speaker_speech_lens'][speaker]]:
                        self.update_occurences(len(lines), superset)

    def resetLasts(self):
        supersets = [self.words, self.line_lens, self.speech_lens]
        for speaker in self.speakers:
            if speaker in ['~null', '~last']:
                continue
            supersets += [self.speaker_words[speaker], self.speaker_line_lens[speaker], self.speaker_speech_lens[speaker]]
        for act in self.play.values():
            for scene in act.values():
                supersets += [scene['words'], scene['line_lens'], scene['speech_lens']]
                for speaker in scene['speakers']:
                    if speaker in ['~null', '~last']:
                        continue
                    supersets += [scene['speaker_words'][speaker], scene['speaker_line_lens'][speaker], scene['speaker_speech_lens'][speaker]]

        for superset in supersets:
            superset['~last'] = '~null'

class Markov:
    def __init__(self, play):
        assert isinstance(play, Play)
        self.play = play

    def findTotal(self, weights):
        total = 0
        for weight in weights:
            if type(weight) == int or type(weight) == float:
                total += weight
        return total

    def pickItem(self, items, lastItem):
        if len(items[lastItem]) == 0:
            lastItem = '~null'
        lastItem = items[lastItem]
        total = self.findTotal(lastItem.values())
        rand = random.random()*total
        for item in lastItem:
            if type(lastItem[item]) == int or type(lastItem[item]) == float:
                if rand<lastItem[item]:
                    return item
                rand -= lastItem[item]

    # correct for special character in the first spot (redo or next)
    def firstWord(self, words, lastWord):
        if all([word in nonwords for word in words[lastWord]]):
            return self.pickItem(words, '~null')

        word = self.pickItem(words, lastWord)
        while word in nonwords:
            word = self.pickItem(words, lastWord)
        return word

    def makeLine(self, words, lineLength, lastWord):
        text = ''
        word = self.firstWord(words, lastWord)
        text += word.capitalize()
        for i in range(lineLength-1):
            word = self.pickItem(words, word)
            text += self.printWord(word)
        return (text, word)

    def makeSpeech(self, words, line_lens, speech_length, lastWord):
        text = '\t'
        lineLength = '~null'
        word = lastWord
        for i in range(speech_length):
            lineLength = self.pickItem(line_lens, lineLength)
            line, word = self.makeLine(words, lineLength, word)
            text += '\t' + self.printLine(line)
        return text + '\n', word

    # Keep last word and lineLength of speaker stored
    # reset last speech_length of each speaker to 0 (every speech check if it's their first in this dialogue)
    def makeDialogue(self, playLength):
        text = ''
        speaker = '~null'
        for act in range(1, playLength + 1):
            text += self.printAct(act)
            act_length = random.choice(self.play.act_lengths)
            for scene in range(1, act_length + 1):
                text += self.printScene(scene)
                scene_length = random.choice(self.play.scene_lengths)
                for speech in range(scene_length):
                    speaker = self.pickItem(self.play.speakers, speaker)
                    speech_length = self.pickItem(self.play.speaker_speech_lens[speaker], self.play.speaker_speech_lens[speaker]['~last'])
                    # print(self.play.speaker_words[speaker])
                    # print(self.play.speaker_line_lens[speaker])
                    speechText, self.play.speaker_words[speaker]['~last'] = self.makeSpeech(self.play.speaker_words[speaker], self.play.speaker_line_lens[speaker], speech_length, self.play.speaker_words[speaker]['~last'])
                    self.play.speaker_speech_lens[speaker]['~last'] = speech_length
                    text += self.printSpeaker(speaker) + speechText
        return text

    def printAct(self, act):
        return 'ACT {}:\n'.format(act)

    def printScene(self, scene):
        return 'SCENE {}:\n'.format(str(scene))

    def printSpeaker(self, speaker):
        return " {}:\n".format(speaker.capitalize())

    def printLine(self, line):
        return line + '\n'

    def printWord(self, word):
        if word in nonwords:
            return word
        elif word == 'i':
            word = 'I'
        elif word[:2] == 'i\'':
            word = 'I\''
        return ' ' + word

    def saveData(self, doc, data):
        output = open(doc,"w")
        output.write(data)

if __name__ == '__main__':
    play = Play('titus.txt')
    markov = Markov(play)
    generated = markov.makeDialogue(4)
    markov.saveData('generated_titus.txt', generated)