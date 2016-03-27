import re, operator
# Markov Chain For Shakespeare Plays
# First Chain: Who is talking - {Othello: {2: Desdemona, 18: Desdemona, ...}, Iago.}

# should line num be half-character
# null: {1: Let}, Let: {1: him}, him, {}
# Range: 1 <= x > x+1/3x
# speakers = {'null': {}, 'Othello': {2: 'Iago', 18: 'Desdemona', ...}, 'Iago': {}}
# speeches = {'Othello': {'lines': {12: 1, 23: 2, 68: 3}, 'words': {'null': {}, 'hi': {'.': 12, 'there'``}, '.':  }}}

def findTotal(weights):
    total = 0
    for weight in weights:
        if type(weight) == int or type(weight) == float:
            total += weight
    return total
def pickItem(lastItem):
    total = findTotal(lastItem)
    rand = random.random()*total
    for weight in lastItem:
        if rand<weight:
            return lastItem[weight]
        rand -= weight
def printSpeaker(speaker):
    return speaker + ':\n'
def makeSpeech(speaker):
    word = speaker['null']
    wordNum = pickItem
def run():
    text = ''
    speaker = pickItem(speakers['null'])
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
    'speaker': r'(\w+):\n',
    'line': r'([^\n]+)\n',
    'stage': r'\[(.*)\]'
}


def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text

# Make lastWord and lastWordNum speaker specific
def textParse(text, form):
    speakers = {'null': {}, 'last': 'null'}
    speeches = {}
    lines = {}
    text = re.sub(form['act'] or form['scene'] or form['stage'], '', text)
    text = re.sub(form['speaker'], r'|speaker|\1|lines|', text)
    speechesText = text.split('|speaker|')[1:]
    for speech in speechesText:
        speakerAndLines = speech.split('|lines|')
        speaker = speakerAndLines[0]
        print speaker
        linesText = speakerAndLines[1].split('\n')[:-1]
        for superset in [speeches, lines]:
            if not speaker in superset:
                superset[speaker] = {'last': 'null'}
        if not speaker in speakers:
            superset[speaker] = {}
        # print speakers['last']
        if not speaker in speakers[speakers['last']]:
            speakers[speakers['last']][speaker] = 0
        speakers[speakers['last']][speaker] += 1
        for line in linesText:
            # words = re.sub('[^a-zA-z-\' ]|\[|\]|--', '', line)
            words = re.sub('([^\'])\b([^\'])', r'\1|break|\2', line)
            words = re.sub(' ', '', words)
            words = words.lower()
            words = words.split('|break|')
            wordNum = 0
            for word in words:
                if r'[^ ]' in word:
                    word = re.sub(' ', '', word)
                    if not word in speeches[speaker]:
                        speeches[speaker][word] = {}
                    if not word in speeches[speaker][speeches[speaker]['last']]:
                        speeches[speaker][speeches[speaker]['last']][word] = 0
                    speeches[speaker][speeches[speaker]['last']][word] += 1
                    speeches[speaker]['last'] = word
                    wordNum += 1
            if not wordNum in lines[speaker]:
                lines[speaker][wordNum] = {}
            if not wordNum in lines[speaker][lines[speaker]['last']]:
                lines[speaker][lines[speaker]['last']][wordNum] = 0
            lines[speaker][lines[speaker]['last']][wordNum] += 1
            lines[speaker]['last'] = wordNum
        speakers['last'] = speaker
    return {'speakers': speakers, 'speeches': speeches, 'lines': lines}

plaintext = openData('text')
text = textParse(plaintext, form)
