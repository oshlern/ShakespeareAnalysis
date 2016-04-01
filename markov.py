import re, random, string
# Markov Chain For Shakespeare Plays
# First Chain: Who is talking - {Othello: {2: Desdemona, 18: Desdemona, ...}, Iago.}

# should line num be half-character
# ~null: {1: Let}, Let: {1: him}, him, {}
# speakers = {'~null': {}, 'Othello': {2: 'Iago', 18: 'Desdemona', ...}, 'Iago': {}}
# speeches = {'Othello': {'lines': {12: 1, 23: 2, 68: 3}, 'words': {'~null': {}, 'hi': {'.': 12, 'there'``}, '.':  }}}
# can Make more sophisticated: what words are said more after certain speakers, speechLengths, etc. or at which point in the speech or dialogue

def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text

# change to if not last in set: set[last] = {}
def textParse(text, form):
    speakers, words, stage = {'~null': {}, '~last': '~null'}, {}, {'words': {}, 'lengths': []}
    playLength, actLengths, sceneLengths, speechLengths, lineLengths = 0, [], [], {}, {}
    text = re.sub('xxx:', '', text)
    text = re.sub('\n\n\n', '\n', text)
    stageText = re.findall(r'\[.*\]', text)
    text = re.sub(r'\[.*\]', '\'stage\'', text)
    for act in re.split(form['act'], text)[1:]:
        actLength = 0
        for scene in re.split(form['scene'], act)[1:]:
            sceneLength = 0
            scene = re.sub(form['speaker'], r'\n|speaker|\1|lines|', scene)
            speeches = scene.split('|speaker|')[1:]
            for speech in speeches:
                speakerAndLines = speech.split('|lines|')
                speaker = speakerAndLines[0]
                lines = speakerAndLines[1].split('\n')[:-1]
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
                    # chars = []
                    # if '|stage|' in line:
                    #     subsections = line.split('|stage|')
                    #     print subsections
                    #     for subsection in subsections:
                    #         subsection = re.sub(r'([^\'])\b([^\'])', r'\1|break|\2', line)
                    #         subsection = re.sub(' ', '', subsection)
                    #         subsection = subsection.lower()
                    #         # print subsection
                    #         chars += subsection.split('|break|') + ['~stage']
                    #     chars.pop() #extra stage
                    # else:
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
    for i in range(len(stageText)):
        chars = re.sub(r'([^\'])\b([^\'])', r'\1|break|\2', stage)
        chars = re.sub(' ', '', chars)
        chars = chars.lower()
        chars = chars.split('|break|')
        length = 0
        for word in chars:
            if not word in stage['words']:
                stage['words'][word] = {}
            if not word in stage['words'][stage['~last']]:
                stage['words'][stage['~last']][word] = 0
            stage['words'][stage['~last']][word] += 1
            stage['~last'] = word
            length += 1
        stage['lengths'] += [length]
    return words, lineLengths, speechLengths, speakers, sceneLengths, actLengths, playLength, stage

def findTotal(weights):
    total = 0
    for weight in weights:
        if type(weight) == int or type(weight) == float:
            total += weight
    return total

def pickItem(items, lastItem):
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

# fix lineBreaks of stage
def makeStage(stage):
    text = ' ['
    stageLength = pickItem(stage, 'lengths')
    word = random.choice(stage['words'].keys())
    text += word
    for i in xrange(stageLength-1):
        word = pickItem(stage['words'], word)
        text += printWord(word)
    return text

# correct for special character in the first spot (redo or next)
def firstWord(words, lastWord):
    word = pickItem(words, lastWord)
    if word in '.,;:-!?_()':
        for word in words[lastWord]:
            if not word in '.,;:-!?_()':
                return word
        return pickItem(words, '~null')
    else:
        return word

def makeLine(words, lineLength, lastWord):
    text = ''
    word = firstWord(words, lastWord)
    text += ' ' + word.capitalize()
    for i in xrange(lineLength-1):
        word = pickItem(words, word)
        text += printWord(word)
    return (text, word)

def makeSpeech(words, lineLengths, speechLength, lastWord):
    text = ''
    lineLength = '~null'
    word = lastWord
    for i in xrange(speechLength):
        lineLength = pickItem(lineLengths, lineLength)
        line, word = makeLine(words, lineLength, word)
        text += printLine(line)
    return text + '\n', word

# Keep last word and lineLength of speaker stored
# reset last speechLength of each speaker to 0 (every speech check if it's their first in this dialogue)
def makeDialogue(words, lineLengths, speechLengths, speakers, sceneLengths, actLengths, playLength):
    text = ''
    speaker = '~null'
    for act in range(1, playLength + 1):
        text += printAct(act)
        actLength = random.choice(actLengths)
        for scene in range(1, actLength + 1):
            text += printScene(scene)
            sceneLength = random.choice(sceneLengths)
            for speech in xrange(sceneLength):
                speaker = pickItem(speakers, speaker)
                speechLength = pickItem(speechLengths[speaker], speechLengths[speaker]['~last'])
                speechText, words[speaker]['~last'] = makeSpeech(words[speaker], lineLengths[speaker], speechLength, words[speaker]['~last'])
                speechLengths[speaker]['~last'] = speechLength
                text += printSpeaker(speaker) + speechText
    return text


form = {
    'act': r'Act \d+:\n',
    'scene': r'Scene \d+:\n',
    'speaker': r'\n([a-z1-9]+):\n',
    'line': r'([^\n]+)\n',
    'stage': r'\[(.*)\]'
}
plaintext = openData('text')
words, lineLengths, speechLengths, speakers, sceneLengths, actLengths, playLength, stage = textParse(plaintext, form)
# print words['emilia']['world']
print makeDialogue(words, lineLengths, speechLengths, speakers, sceneLengths, actLengths, 1)
# print text['words']['iago']['is']
# print speechLengths
