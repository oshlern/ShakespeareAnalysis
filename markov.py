import re, random
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
    speakers = {'~null': {}, '~last': '~null'}
    words = {}
    speechLengths = {}
    lineLengths = {}
    # text = re.sub(form['act'] or form['scene'] or form['stage'] or 'xxx:', '', text)
    text = re.sub(form['act'], '', text)
    text = re.sub(form['scene'], '', text)
    text = re.sub(form['stage'], '', text)
    text = re.sub('xxx:', '', text)
    text = re.sub('\n\n\n', '\n', text)
    text = re.sub(form['speaker'], r'\n|speaker|\1|lines|', text)
    speeches = text.split('|speaker|')[1:]
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
    # for speaker in speakers:

    # return {'speakers': speakers, 'words': words, 'lineLengths': lineLengths, 'speechLengths': speechLengths}
    return (speakers, words, lineLengths, speechLengths)

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

def printSpeaker(speaker):
    return speaker + ':\n'

def printWord(word):
    if word in '.,;:-!?_()':
        return word
    return ' ' + word

def printLine(line):
    return line + '\n'

# Add acts and scenes

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
    text += printWord(word)
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
    return text, word

# Keep last word and lineLength of speaker stored
# reset last speechLength of each speaker to 0 (every speech check if it's their first in this dialogue)
def makeDialogue(words, lineLengths, speechLengths, speakers, speechNum):
    text = ''
    speaker = '~null'
    for i in xrange(speechNum):
        speaker = pickItem(speakers, speaker)
        speechLength = pickItem(speechLengths[speaker], speechLengths[speaker]['~last'])
        speech, words[speaker]['~last'] = makeSpeech(words[speaker], lineLengths[speaker], speechLength, words[speaker]['~last'])
        speechLengths[speaker]['~last'] = speechLength
        text += printSpeaker(speaker) + speech
    return text


form = {
    'act': r'Act \d+:\n',
    'scene': r'Scene \d+:\n',
    'speaker': r'\n([a-z1-9]+):\n',
    'line': r'([^\n]+)\n',
    'stage': r'\[(.*)\]'
}
plaintext = openData('text')
speakers, words, lineLengths, speechLengths = textParse(plaintext, form)
# print words['emilia']['world']
print makeDialogue(words, lineLengths, speechLengths, speakers, 300)
# print text['words']['iago']['is']
# print speechLengths
