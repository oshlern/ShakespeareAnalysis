# Category = {plaintext, subsets, analysis}
# analysis = {actNum, sceneNum, speechNum, lineNum, wordNum, charNum, speakerNum}
# make one for chapters and pages
import re
# form = {'text': 'act\nscene\nspeaker:\nspeech', 'act': 'Act [0-9]*', 'scene': 'Scene #', 'speaker': 'XXX:\n'}
# fix formatingg
# [0 lineNum, 1 'Speaker', 2 'Text', 3 actNum, 4 sceneNum, 5 charNum, 6 wordNum],
# [3676, 'othello', 'O villain!\n', ' O FLN ', ' o villain ', 5, 2, 11, 2],
# def appearNum(str, substr):
#     return(len(re.finditer(substr, str)))
def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text

def textFormat(text, form):
    text = {'text': text}
    #act = {re.form['act']: '@ |'}
    # stage = text    #make a parser to separate the state instructions from stats
    # stage = re.sub('.*[([.*]).*]*')
    # def splitBy(text, form):
    #     text = re.sub(form, '\1\|', text)
    #     text = re.split('\|', text)[1:]
    # correct capitalization for speakers
    text['acts'] = re.split(form['act'], text['text'])[1:]
    for actNum in range(len(text['acts'])):
        act = text['acts'][actNum]
        act = {'text': act, 'scenes': re.split(form['scene'], act)[1:]}
        for sceneNum in range(len(act['scenes'])):
            scene = {'text': act['scenes'][sceneNum]}
            scene['speeches'] = scene['text'].split('|speaker|', re.sub(form['speaker'], '\|speaker\|$1\|lines\|'))
            for speechNum in range(len(scene['speeches'])):
                speech = {'text': scene['speeches'][speechNum]}
                speakerAndLines = speech['text'].split('|lines|')
                speech['speaker'] = speakerAndLines[0]
                speech['lines'] = speakerAndLines[1]

    # text = re.sub('(.*):\n', '\|\1@\n', text)
    # text = text.split('|')
    return text

def speechFormat(speech, totalLineNum):
    # speech = {'speaker': speech[0], 'text': speech[1]}
    speech['totalLineNum'] = totalLineNum
    speech['lines'] = speech['text'].split('\n')
    speech['lines'].pop()
    speech['lines']=[]
    for lineNum in range(len(speech['text'])):
        speech['lines'][lineNum] = {'line': lineNum, 'text': speech['text'][lineNum]}
    speech['lineNum'] = len(re.finditer('\n', speech['text']))
    speech['wordNum'] = len(re.finditer(' ', speech['text']))+speech['lineNum']
    speech['charNum'] = len(speech['text'])-speech['lineNum']
    # add acts and scenes
    # add line numbers to speech[]'text']
    totalLineNum+ = speech['lineNum']
    return speech

def getData():
    form = {'act': 'Act \d*:\n', 'scene': 'Scene \d*:\n', 'speaker': '([^\n]+):\n'}
    # form['speech'] = form['speaker']+''
    text = openData('trueothello')
    text = textFormat(text, form)

    # varDec()
    sortedText = {}
    chars = {}

    currentAct = 0
    currentScene = 0
    totalLineNum = 1

    for actNum in range(len(text['acts'])):
        act = text['acts'][actNum]
        for sceneNum in range(len(act['scenes'])):
            scene = act['scenes'][sceneNum]
            for speechNum in range(len(scene['speeches'])):
                speech = scene['speeches'][speechNum]
                speech = speechFormat(speech, totalLineNum)
                text[i] = speech
                # totalLineNum = speech['totalLineNum']
                speaker = speech['speaker']
                # text = speech['text']
                act = speech['act']
                scene = speech['scene']
                # charNum = speech['charNum']
                # wordNum = speech['wordNum']

                if not speaker in chars:
                    chars[speaker] = {act: {scene: []}}

                if act! = currentAct:
                    currentAct = act
                    sortedText[act] = {}
                    for char in chars.keys():
                        chars[char][act] = {scene: []}

                if scene! = currentScene:
                    currentScene = scene
                    sortedText[act][scene] = []
                    for char in chars.keys():
                        chars[char][act][scene] = []

                chars[speaker][act][scene].append({'totalLineNum': speech['totalLineNum'], 'text': speech['text'], 'charNum': speech['charNum'], 'wordNum': speech['wordNum']})
                sortedText[act][scene].append({'totalLineNum': speech['totalLineNum'], 'speaker': speaker, 'text': speech['text'], 'charNum': speech['charNum'], 'wordNum': speech['wordNum']})
    return {'text': text, 'chars': chars}
data = getData()
# text = data['text']
# chars = data['chars']
print chars['iago'][2][1]


# get acts and scenes in raw data
