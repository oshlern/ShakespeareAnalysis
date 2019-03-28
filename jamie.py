import re, random
# Markov Chain For Shakespeare Plays
# First Chain: Who is talking - {Othello: {2: Desdemona, 18: Desdemona, ...}, Iago.}

# should line num be half-character
# ~null: {1: Let}, Let: {1: him}, him, {}
# speakers = {'~null': {}, 'Othello': {2: 'Iago', 18: 'Desdemona', ...}, 'Iago': {}}
# speeches = {'Othello': {'lines': {12: 1, 23: 2, 68: 3}, 'words': {'~null': {}, 'hi': {'.': 12, 'there'``}, '.':  }}}
# can Make more sophisticated: what words are said more after certain speakers, speechLengths, etc. or at which point in the speech or dialogue

class Play:
    def __init__(self, doc):
        self.openDoc()

        self.speakers = {'~null': {}, '~last': '~null'}
        self.words = {}
        self.playLength = 0
        self.actLengths = []
        self.sceneLengths = []
        self.speechLengths = {}
        self.lineLengths = {}

    def openDoc(self, doc):
        text = open(doc, 'r')
        self.text = text.read()

    def saveData(self, doc, data):
        output = open(doc,"w")
        output.write(data)

    # change to if not last in set: set[last] = {}
    def textParse(self, text):
        form = {
            'act': r'ACT \w+\. ',
            'scene': r'SCENE \w+\.\n',
            'speaker': r'\n  ([A-Z1-9 ]+)\. ',
            'line': r'([^\n]+)\n',
            'stage': r'\[(.*)\]'
        }

        # Remove stage directions
        text = re.sub(r'\[[^\]]*\]', '', text)
        # stageText = re.findall(r'\[.*\]', flags=re.DOTALL)
        for act_num, act in enumerate(re.split('|act|', text)[1:]):
            self.play[act_num] = {}
            for scene_num, scene in enumerate(re.split('|scene|', act)[1:]):
                self.play[act_num][scene_num] = {}
                speeches = scene.split('|speaker|')[1:]
                for speech in speeches:
                    speaker, lines = speech.split('|lines|')
                    lines = lines.split('\n')[:-1]
                    for superset in [words, lineLengths, speechLengths]:
                        if not speaker in superset:
                            superset[speaker] = {'~null': {}, '~last': '~null'}
                    if not speaker in speakers:
                        speakers[speaker] = {}
                    if not speaker in speakers[speakers['~last']]:
                        speakers[speakers['~last']][speaker] = 0
                    speakers[speakers['~last']][speaker] += 1
                    lineNum = 0
                    for line in lines:
                        # chars = re.sub(r'([a-zA-z-\'])([^a-zA-z-\'])', r'\1', line)
                        chars = re.sub(r'([^\'])\b([^\'])', r'\1|break|\2', line)
                        chars = re.sub(' ', '', chars)
                        chars = chars.lower()
                        chars = chars.split('|break|')
                        wordNum = 0
                        for word in chars:
                            if not word in words[speaker]:
                                words[speaker][word] = {}
                            if not word in words[speaker][words[speaker]['~last']]:
                                words[speaker][words[speaker]['~last']][word] = 0
                            words[speaker][words[speaker]['~last']][word] += 1
                            words[speaker]['~last'] = word
                            wordNum += 1
                        if not wordNum in lineLengths[speaker]:
                            lineLengths[speaker][wordNum] = {}
                        if not wordNum in lineLengths[speaker][lineLengths[speaker]['~last']]:
                            lineLengths[speaker][lineLengths[speaker]['~last']][wordNum] = 0
                        lineLengths[speaker][lineLengths[speaker]['~last']][wordNum] += 1
                        lineLengths[speaker]['~last'] = wordNum
                        lineNum += 1
                    if not lineNum in speechLengths[speaker]:
                        speechLengths[speaker][lineNum] = {}
                    if not lineNum in speechLengths[speaker][speechLengths[speaker]['~last']]:
                        speechLengths[speaker][speechLengths[speaker]['~last']][lineNum] = 0
                    speechLengths[speaker][speechLengths[speaker]['~last']][lineNum] += 1
                    speechLengths[speaker]['~last'] = lineNum
                    speakers['~last'] = speaker
                    sceneLength += 1
                sceneLengths += [sceneLength]
                actLength += 1
            actLengths += [actLength]
            playLength += 1
    # text = re.sub(form['act'], '', text)
    # text = re.sub(form['scene'], '', text)
    # text = re.sub(form['stage'], '', text)
    #
    # speeches = text.split('|speaker|')[1:]
    # for speech in speeches:
    #     speakerAndLines = speech.split('|lines|')
    #     speaker = speakerAndLines[0]
    #     lines = speakerAndLines[1].split('\n')[:-1]
    #     for superset in [words, lineLengths, speechLengths]:
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
    #         if not wordNum in lineLengths[speaker]:
    #             lineLengths[speaker][wordNum] = {}
    #         if not wordNum in lineLengths[speaker][lineLengths[speaker]['~last']]:
    #             lineLengths[speaker][lineLengths[speaker]['~last']][wordNum] = 0
    #         lineLengths[speaker][lineLengths[speaker]['~last']][wordNum] += 1
    #         lineLengths[speaker]['~last'] = wordNum
    #         lineNum += 1
    #     if not lineNum in speechLengths[speaker]:
    #         speechLengths[speaker][lineNum] = {}
    #     if not lineNum in speechLengths[speaker][speechLengths[speaker]['~last']]:
    #         speechLengths[speaker][speechLengths[speaker]['~last']][lineNum] = 0
    #     speechLengths[speaker][speechLengths[speaker]['~last']][lineNum] += 1
    #     speechLengths[speaker]['~last'] = lineNum
    #     speakers['~last'] = speaker
    # for speaker in speakers:

    # return {'speakers': speakers, 'words': words, 'lineLengths': lineLengths, 'speechLengths': speechLengths}
    return words, lineLengths, speechLengths, speakers, sceneLengths, actLengths, playLength

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
        total = findTotal(lastItem.values())
        rand = random.random()*total
        for item in lastItem:
            if type(lastItem[item]) == int or type(lastItem[item]) == float:
                if rand<lastItem[item]:
                    return item
                rand -= lastItem[item]

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

    def makeSpeech(self, words, lineLengths, speechLength, lastWord):
        text = ''
        lineLength = '~null'
        word = lastWord
        for i in range(speechLength):
            lineLength = self.pickItem(lineLengths, lineLength)
            line, word = makeLine(words, lineLength, word)
            text += printLine(line)
        return text + '\n', word

    # Keep last word and lineLength of speaker stored
    # reset last speechLength of each speaker to 0 (every speech check if it's their first in this dialogue)
    def makeDialogue(self, words, lineLengths, speechLengths, speakers, sceneLengths, actLengths, playLength):
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
                    speechLength = self.pickItem(speechLengths[speaker], speechLengths[speaker]['~last'])
                    speechText, words[speaker]['~last'] = makeSpeech(words[speaker], lineLengths[speaker], speechLength, words[speaker]['~last'])
                    speechLengths[speaker]['~last'] = speechLength
                    text += printSpeaker(speaker) + speechText
        return text


# print words['emilia']['world']



# play = makeDialogue(words, lineLengths, speechLengths, speakers, sceneLengths, actLengths, 1)
# saveData("generated", play)
# print play
# print text['words']['iago']['is']
# print speechLengths
