import re, operator
# Markov Chain For Shakespeare Plays
# First Chain: Who is talking - {Othello: {2: Desdemona, 18: Desdemona, ...}, Iago.}

# should line num be half-character
# ~null: {1: Let}, Let: {1: him}, him, {}
# Range: 1 <= x > x+1/3x
# speakers = {'~null': {}, 'Othello': {2: 'Iago', 18: 'Desdemona', ...}, 'Iago': {}}
# speeches = {'Othello': {'lines': {12: 1, 23: 2, 68: 3}, 'words': {'~null': {}, 'hi': {'.': 12, 'there'``}, '.':  }}}

def findTotal(weights):
    total = 0
    for weight in weights:
        if type(weight) == int or type(weight) == float:
            total += weight
    return total
def pickItem(lastItem):
    total = findTotal(lastItem.items())
    rand = random.random()*total
    for item in lastItem:
        if rand<lastItem[item]:
            return item
        rand -= lastItem[item]
def printSpeaker(speaker):
    return speaker + ':\n'
def printWord(word):
    if word == r'[^\w\']':
        return word
    return ' ' + word
def printLine():
    return '\n'
def makeLine(words, lineLength):
    word = '~null'
def makeSpeech(words, lineLengths, speechLength):
    word = '~null'
    wordNum = pickItem
def makeDialogue(words, lineLengths, speechLengths, speakers):
    text = ''
    speaker = pickItem(speakers['~null'])
    for speech in range(100):
        text += printSpeaker(speaker)
        speaker = speakers[speaker]


# Treat punctuation and new lines as a word
# Markov per character
# Markov for which character
# Markov
# make prints
# fix stage instructions

# Make Markov Chains
# fix line spacing with tabs
# make a parser to separate the stage instructions from stats
# char count w/ speakers?
# fix general char count (not chars)

form = {
    'act': r'Act \d+:\n',
    'scene': r'Scene \d+:\n',
    'speaker': r'\n([a-z1-9]+):\n',
    'line': r'([^\n]+)\n',
    'stage': r'\[(.*)\]'
}


def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text

# Make lastWord and lastWordNum speaker specific
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
        for superset in [words, lineLengths]:
            if not speaker in superset:
                superset[speaker] = {'~null': {}, '~last': '~null'}
        if not speaker in speakers:
            speakers[speaker] = {}
        if not speaker in speakers[speakers['~last']]:
            speakers[speakers['~last']][speaker] = 0
        speakers[speakers['~last']][speaker] += 1
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
        speakers['~last'] = speaker
    return {'speakers': speakers, 'words': words, 'lines': lineLengths}

plaintext = openData('text')
text = textParse(plaintext, form)
# print text['words']['iago']['is']
