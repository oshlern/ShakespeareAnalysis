import re, random, preprocess
# Markov Chain For Shakespeare Plays
# First Chain: Who is talking - {Othello: {2: Desdemona, 18: Desdemona, ...}, Iago.}

# should line num be half-character
# ~null: {1: Let}, Let: {1: him}, him, {}
# speakers = {'~null': {}, 'Othello': {2: 'Iago', 18: 'Desdemona', ...}, 'Iago': {}}
# speeches = {'Othello': {'lines': {12: 1, 23: 2, 68: 3}, 'words': {'~null': {}, 'hi': {'.': 12, 'there'``}, '.':  }}}
# can Make more sophisticated: what words are said more after certain speakers, speech_lens, etc. or at which point in the speech or dialogue

class Play:
    def __init__(self, doc):
        self.openDoc(doc)

        self.speakers = {'~null': {}, '~last': '~null'}
        self.play = {}

        self.actLengths = []
        self.sceneLengths = []
        self.speech_lens = {}
        self.line_lens = {}
        self.words = {}

        self.parseText()

    def openDoc(self, doc):
        processed_file = "processed_" + doc
        preprocess.preprocess(doc, processed_file)
        processed = open(processed_file, 'r')
        self.text = processed.read()

    def saveData(self, doc, data):
        output = open(doc,"w")
        output.write(data)

    def update_occurences(self, item, superset):
        if not item in superset:
            superset[item] = {}
        superset[superset['~last']][item] = 1 + superset[superset['~last']].get(item, 0)
        superset['~last'] = item

    # change to if not last in set: set[last] = {}
    def parseText(self):
        # print(re.split('|act|', self.text)[1:])
        # print(self.text[1000:10000])
        for act_num, act in enumerate(self.text.split('|act|')[1:]):
            self.play[act_num] = {}
            for scene_num, scene in enumerate(act.split('|scene|')[1:]):
                self.play[act_num][scene_num] = {}
                speeches = scene.split('|speaker|')[1:]
                for speech in speeches:
                    speaker, lines = speech.split('|lines|')
                    lines = lines.split('\n')[:-1]

                    # Initialize speaker
                    for superset in [self.words, self.line_lens, self.speech_lens]:
                        if not speaker in superset:
                            superset[speaker] = {'~null': {}, '~last': '~null'}
                    self.update_occurences(speaker, self.speakers)
                    # if not speaker in self.speakers:
                    #     self.speakers[speaker] = {}
                    # self.speakers[self.speakers['~last']][speaker] = 1 + self.speakers[self.speakers['~last']].get(speaker,0)
                    for line in lines:
                        # if random.random() < 0.5:
                        # print("TEST", line)
                        chars = re.sub(r'([a-zA-z-\'])([^a-zA-z-\'])', r'\1', line)
                        chars = re.sub(r'([^\'])\b([^\'])', r'\1|word_break|\2', line)
                        chars = re.sub(' ', '', chars)
                        chars = chars.lower()
                        words = chars.split('|word_break|')
                        for word in words:
                            self.update_occurences(word, self.words[speaker])
                            # if not word in self.words[speaker]:
                            #     self.words[speaker][word] = {}
                            # self.words[speaker][self.words[speaker]['~last']][word] = 1 + self.words[speaker][self.words[speaker]['~last']].get(word,0)
                            # self.words[speaker]['~last'] = word
                        self.update_occurences(len(words), self.line_lens[speaker])
                        # line_len = len(words)
                        # if not line_len in self.line_lens[speaker]:
                        #     self.line_lens[speaker][line_len] = {}
                        # self.line_lens[speaker][self.line_lens[speaker]['~last']][line_len] = 1 + self.line_lens[speaker][self.line_lens[speaker]['~last']].get(line_len, 0)
                        # self.line_lens[speaker]['~last'] = line_len
                    self.update_occurences(len(lines), self.speech_lens[speaker])
                    # line_num = len(lines)
                    # if not line_num in speech_lens[speaker]:
            #             speech_lens[speaker][lineNum] = {}
            #         if not lineNum in speech_lens[speaker][speech_lens[speaker]['~last']]:
            #             speech_lens[speaker][speech_lens[speaker]['~last']][lineNum] = 0
            #         speech_lens[speaker][speech_lens[speaker]['~last']][lineNum] += 1
            #         speech_lens[speaker]['~last'] = lineNum
            #         speakers['~last'] = speaker
            #         sceneLength += 1
            #     sceneLengths += [sceneLength]
            #     actLength += 1
            # actLengths += [actLength]
    # text = re.sub(form['act'], '', text)
    # text = re.sub(form['scene'], '', text)
    # text = re.sub(form['stage'], '', text)
    #
    # speeches = text.split('|speaker|')[1:]
    # for speech in speeches:
    #     speakerAndLines = speech.split('|lines|')
    #     speaker = speakerAndLines[0]
    #     lines = speakerAndLines[1].split('\n')[:-1]
    #     for superset in [words, line_lens, speech_lens]:
    #         if not speaker in superset:
    #             superset[speaker] = {'~null': {}, '~last': '~null'}
    #     if not speaker in speakers:
    #         speakers[speaker] = {}
    #     if not speaker in speakers[speakers['~last']]:
    #         speakers[speakers['~last']][speaker] = 0
    #     speakers[speakers['~last']][speaker] += 1
    #     lineNum = 0
    #     for line in lines:
    #         # chars = re.sub(r'([a-zA-z-\'])([^a-zA-z-\'])', r'\1', line)
    #         chars = re.sub(r'([^\'])\b([^\'])', r'\1|break|\2', line)
    #         chars = re.sub(' ', '', chars)
    #         chars = chars.lower()
    #         chars = chars.split('|break|')
    #         wordNum = 0
    #         for word in chars:
    #             if not word in words[speaker]:
    #                 words[speaker][word] = {}
    #             if not word in words[speaker][words[speaker]['~last']]:
    #                 words[speaker][words[speaker]['~last']][word] = 0
    #             words[speaker][words[speaker]['~last']][word] += 1
    #             words[speaker]['~last'] = word
    #             wordNum += 1
    #         if not wordNum in line_lens[speaker]:
    #             line_lens[speaker][wordNum] = {}
    #         if not wordNum in line_lens[speaker][line_lens[speaker]['~last']]:
    #             line_lens[speaker][line_lens[speaker]['~last']][wordNum] = 0
    #         line_lens[speaker][line_lens[speaker]['~last']][wordNum] += 1
    #         line_lens[speaker]['~last'] = wordNum
    #         lineNum += 1
    #     if not lineNum in speech_lens[speaker]:
    #         speech_lens[speaker][lineNum] = {}
    #     if not lineNum in speech_lens[speaker][speech_lens[speaker]['~last']]:
    #         speech_lens[speaker][speech_lens[speaker]['~last']][lineNum] = 0
    #     speech_lens[speaker][speech_lens[speaker]['~last']][lineNum] += 1
    #     speech_lens[speaker]['~last'] = lineNum
    #     speakers['~last'] = speaker
    # for speaker in speakers:

    # return {'speakers': speakers, 'words': words, 'line_lens': line_lens, 'speech_lens': speech_lens}
    # return words, line_lens, speech_lens, speakers, sceneLengths, actLengths, playLength

def printAct(act):
    return '                 ACT ' + str(act) + ':\n'

def printScene(scene):
    return '                SCENE ' + str(scene) + ':\n'

def printSpeaker(speaker):
    return speaker.capitalize() + ':\n'

def printLine(line):
    return line + '\n'

def printWord(word):
    if word in '.,;:-!?_()':
        return word
    elif word == 'i':
        word = 'I'
    elif word[:2] == 'i\'':
        word = 'I\''
    return ' ' + word

class Markov:
    def __init__(play):
        assert isinstance(play, Play)

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
        word = self.pickItem(words, lastWord)
        if word in '.,;:-!?_()':
            for word in words[lastWord]:
                if not word in '.,;:-!?_()':
                    return word
            return self.pickItem(words, '~null')
        else:
            return word

    def makeLine(self, words, lineLength, lastWord):
        text = ''
        word = self.firstWord(words, lastWord)
        text += ' ' + word.capitalize()
        for i in range(lineLength-1):
            word = self.pickItem(words, word)
            text += printWord(word)
        return (text, word)

    def makeSpeech(self, words, line_lens, speechLength, lastWord):
        text = ''
        lineLength = '~null'
        word = lastWord
        for i in range(speechLength):
            lineLength = self.pickItem(line_lens, lineLength)
            line, word = makeLine(words, lineLength, word)
            text += printLine(line)
        return text + '\n', word

    # Keep last word and lineLength of speaker stored
    # reset last speechLength of each speaker to 0 (every speech check if it's their first in this dialogue)
    def makeDialogue(self, words, line_lens, speech_lens, speakers, sceneLengths, actLengths, playLength):
        text = ''
        speaker = '~null'
        for act in range(1, playLength + 1):
            text += printAct(act)
            actLength = random.choice(actLengths)
            for scene in range(1, actLength + 1):
                text += printScene(scene)
                sceneLength = random.choice(sceneLengths)
                for speech in range(sceneLength):
                    speaker = self.pickItem(speakers, speaker)
                    speechLength = self.pickItem(speech_lens[speaker], speech_lens[speaker]['~last'])
                    speechText, words[speaker]['~last'] = makeSpeech(words[speaker], line_lens[speaker], speechLength, words[speaker]['~last'])
                    speech_lens[speaker]['~last'] = speechLength
                    text += printSpeaker(speaker) + speechText
        return text


# print words['emilia']['world']

play = Play('titus.txt')

# play = makeDialogue(words, line_lens, speech_lens, speakers, sceneLengths, actLengths, 1)
# saveData("generated", play)
# print play
# print text['words']['iago']['is']
# print speech_lens
