# properties = {actNum, sceneNum, speechNum, lineNum, wordNum, charNum, speakerNum}
# fix line spacing with tabs
import re
# Make print function to replace the 99.99% of storage used by deleting plaintext for everything but characters and speakers
# change variables of currentLineNum and such to changing variables within the dictionary
form = {'act': r'Act \d+:\n', 'scene': r'Scene \d+:\n', 'speaker': r'(\w+):\n', r'line': '(1^\n]+)\n'}

# def appearNum(str, substr):
#     return(len(re.finditer(substr, str)))
def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text

def textParse(text, form):
    text = {'plaintext': text}

    totalLineNum = 0
    totalSpeechNum = 0
    totalSceneNum = 0
    # total = {charNum, wordNum, lineNum, speechNum, sceneNum}
    # text['properties'] = {charNum, wordNum, lineNum, speechNum, sceneNum}
    speakers = {}
    #make a parser to separate the state instructions from stats
    text['acts'] = re.split(form['act'], text['plaintext'])[1:]
    text['properties'] = {'lengthActs': len(text['acts']), 'lengthScenes': 0, 'lengthSpeeches': 0, 'lengthLines': 0, 'lengthWords': 0, 'lengthChars': 0}
    for actNum in range(text['properties']['lengthActs']):
        act = text['acts'][actNum]
        act = {'plaintext': act, 'scenes': re.split(form['scene'], act)[1:]}
        act['properties'] = {'lengthScenes': len(act['scenes'])}
        act['properties']['startLine'] = text['properties']['lengthLines']
        act['properties']['startSpeech'] = text['properties']['lengthSpeeches']
        # actLineStart = text['properties']['lengthLines']
        # start = {'act': [charNum, wrodNum, lineNum, speechNum, sceneNum], }
        for sceneNum in range(act['properties']['lengthScenes']):
            scene = {'plaintext': act['scenes'][sceneNum]}
            speakerForm = re.sub(form['speaker'], r'|speaker|\1|lines|', scene['plaintext'])
            scene['speeches'] = speakerForm.split('|speaker|')[1:]
            scene['properties'] = {'lengthSpeeches': len(scene['speeches']), 'startTotalLineNum': totalLineNum}
            totalSpeechNum += scene['properties']['lengthSpeeches']
            currentLineNum = 0
            for speechNum in range(scene['properties']['lengthSpeeches']):
                # speech = {'plaintext': scene['speeches'][speechNum]} # plaintext has |lines|
                speakerAndLines = scene['speeches'][speechNum].split('|lines|')
                # speech['plaintext'] = re.sub('\|lines\|', '', speech['plaintext'])
                speech = {'speaker': speakerAndLines[0]}
                speech['plaintext'] = speech['speaker']+':\n'+speakerAndLines[1]
                speech['lines'] = speakerAndLines[1].split('\n')
                speech['lines'].pop() #extra newline on the end
                speech['properties'] = {'startLineNum': currentLineNum, 'startTotalLineNum': totalLineNum, 'lengthLines': len(speech['lines'])}
                for lineNum in range(speech['properties']['lengthLines']):
                    currentLineNum += 1
                    totalLineNum += 1
                    line = {'plaintext': speech['lines'][lineNum]}
                    line['properties'] = {'lineNum': currentLineNum, 'totalLineNum': totalLineNum}
                    speech['lines'][lineNum] = line
                    # figure out how to split into words when using punctuation and hyphens
                speech['properties']['endLineNum'] = currentLineNum
                speech['properties']['endTotalLineNum'] = totalLineNum
                # speechNum
                scene['speeches'][speechNum] = speech
            scene['properties']['lengthLines'] = currentLineNum
            scene['properties']['endTotalLineNum'] = totalLineNum
            act['scenes'][sceneNum] = scene
        act['properties']['lengthLines'] = totalLineNum-act['properties']['startLine']
        act['properties']['lengthSpeeches'] = totalSpeechNum-act['properties']['startSpeech']
        text['acts'][actNum] = act
    text['properties']['lengthLines'] = totalLineNum
    text['properties']['lengthSpeeches'] = totalSpeechNum
    text['properties']['lengthScenes'] = totalSceneNum
    # generalize the format and include different ones so that you can make a recursive function for the for loops
    return text

text = openData('text')
data = textParse(text, form)

# print data['acts'][1]['scenes'][0]['speeches'][13]['plaintext']
print data['properties']
