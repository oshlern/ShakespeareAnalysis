# properties = {actNum, sceneNum, speechNum, lineNum, wordNum, charNum, speakerNum}
import re

form = {'act': r'Act \d+:\n', 'scene': r'Scene \d+:\n', 'speaker': r'\|(\w+):\n', r'line': '(1^\n]+)\n'}

# def appearNum(str, substr):
#     return(len(re.finditer(substr, str)))
def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text

def textParse(text, form):
    text = {'plaintext': text}

    totalLineNum = 1
    speakers = {}
    #make a parser to separate the state instructions from stats
    text['acts'] = re.split(form['act'], text['plaintext'])[1:]
    # print text['plaintext']
    # print text['acts']
    # print form['act']
    for actNum in range(len(text['acts'])):
        act = text['acts'][actNum]
        act = {'plaintext': act, 'scenes': re.split(form['scene'], act)[1:]}
        # print act
        for sceneNum in range(len(act['scenes'])):
            scene = {'plaintext': act['scenes'][sceneNum]}
            speakerForm = re.sub(form['speaker'], r'|speaker|\1|lines|', scene['plaintext'])
            # print speakerForm
            scene['speeches'] = speakerForm.split('|speaker|')[1:]
            scene['properties'] = {'lengthSpeeches': len(scene['speeches'])}
            currentLineNum = 1
            # print scene
            for speechNum in range(scene['properties']['lengthSpeeches']):
                speech = {'plaintext': scene['speeches'][speechNum]}
                # print  speech
                speakerAndLines = speech['plaintext'].split('|lines|')
                # print speakerAndLines
                # print '\n'
                speech['speaker'] = speakerAndLines[0]
                speech['speech'] = {'plaintext': speakerAndLines[1]}
                speech['speech']['lines'] = speech['speech']['plaintext'].split('\n')
                speech['speech']['lines'].pop()
                speech['properties'] = {'startLineNum': currentLineNum, 'startTotalLineNum': totalLineNum, 'lengthLines': len(speech['speech']['lines'])}
                for lineNum in range(speech['properties']['lengthLines']):
                    line = {'plaintext': speech['speech']['lines'][lineNum]}
                    line['properties'] = {'lineNum': currentLineNum, 'totalLineNum': totalLineNum}
                    currentLineNum += 1
                    totalLineNum += 1
                    speech['speech']['lines'][lineNum] = line
                # speech['properties']['lengthLines'] = currentLineNum - speech['properties'][startLineNum]
                speech['properties']['endLineNum'] = currentLineNum-1
                speech['properties']['endTotalLineNum'] = currentLineNum-1
                scene['speeches'][speechNum] = speech
            scene['properties']['lengthLines'] = currentLineNum
                    # figure out how to split into words when using punctuation and hyphens

            scene['speeches'][speechNum] = speech
            act['scenes'][sceneNum] = scene
        text['acts'][actNum] = act


    # generalize the format and include different ones so that you can make a recursive function for the for loops
    # text = re.sub('(.*):\n', '\|\1@\n', text)
    # text = text.split('|')
    return text

# def speechFormat(speech, totalLineNum):
#     # speech = {'speaker': speech[0], 'plaintext': speech[1]}
#     speech['totalLineNum'] = totalLineNum
#     speech['lines'] = speech['plaintext'].split('\n')
#     speech['lines'].pop()
#     speech['lines']=[]
#     for lineNum in range(len(speech['plaintext'])):
#         speech['lines'][lineNum] = {'line': lineNum, 'plaintext': speech['plaintext'][lineNum]}
#     speech['lineNum'] = len(re.finditer('\n', speech['plaintext']))
#     speech['wordNum'] = len(re.finditer(' ', speech['plaintext']))+speech['lineNum']
#     speech['charNum'] = len(speech['plaintext'])-speech['lineNum']
#     # add acts and scenes
#     # add line numbers to speech[]'plaintext']
#     totalLineNum+ = speech['lineNum']
#     return speech
#
# def getData():
#     # lose case sensitivity of acts and scenes
#     # convert to Xxx case sensitivity
#     # form['speech'] = form['speaker']+''
text = openData('text')
data = textParse(text, form)
#
#     # varDec()
#     sortedText = {}
#     chars = {}
#
#     currentAct = 0
#     currentScene = 0
#     totalLineNum = 1
#
#     for actNum in range(len(text['acts'])):
#         act = text['acts'][actNum]
#         for sceneNum in range(len(act['scenes'])):
#             scene = act['scenes'][sceneNum]
#             for speechNum in range(len(scene['speeches'])):
#                 speech = scene['speeches'][speechNum]
#                 speech = speechFormat(speech, totalLineNum)
#                 text[i] = speech
#                 # totalLineNum = speech['totalLineNum']
#                 speaker = speech['speaker']
#                 # text = speech['plaintext']
#                 act = speech['act']
#                 scene = speech['scene']
#                 # charNum = speech['charNum']
#                 # wordNum = speech['wordNum']
#
#                 if not speaker in chars:
#                     chars[speaker] = {act: {scene: []}}
#
#                 if act! = currentAct:
#                     currentAct = act
#                     sortedText[act] = {}
#                     for char in chars.keys():
#                         chars[char][act] = {scene: []}
#
#                 if scene! = currentScene:
#                     currentScene = scene
#                     sortedText[act][scene] = []
#                     for char in chars.keys():
#                         chars[char][act][scene] = []
#
#                 chars[speaker][act][scene].append({'totalLineNum': speech['totalLineNum'], 'plaintext': speech['plaintext'], 'charNum': speech['charNum'], 'wordNum': speech['wordNum']})
#                 sortedText[act][scene].append({'totalLineNum': speech['totalLineNum'], 'speaker': speaker, 'plaintext': speech['plaintext'], 'charNum': speech['charNum'], 'wordNum': speech['wordNum']})
#     return {'text': text, 'chars': chars}
# text = data['text']
# chars = data['chars']
print data['acts'][1]['scenes'][0]['speeches'][13]

# get acts and scenes in raw data
