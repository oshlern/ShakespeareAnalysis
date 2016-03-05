# properties = {actNum, sceneNum, speechNum, lineNum, wordNum, charNum, speakerNum}
# fix line spacing with tabs
import re

form = {'act': r'Act \d+:\n', 'scene': r'Scene \d+:\n', 'speaker': r'(\w+):\n', r'line': '(1^\n]+)\n'}

# def appearNum(str, substr):
#     return(len(re.finditer(substr, str)))
def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text

def textParse(text, form):
    text = {'plaintext': text}

    totalLineNum = 1
    totalSpeechNum = 1
    totalSceneNum = 1
    speakers = {}
    #make a parser to separate the state instructions from stats
    text['acts'] = re.split(form['act'], text['plaintext'])[1:]
    text['properties'] = {'lengthActs': len(text['acts'])}
    for actNum in range(text['properties']['lengthActs']):
        act = text['acts'][actNum]
        act = {'plaintext': act, 'scenes': re.split(form['scene'], act)[1:]}
        act['properties'] = {'lengthScenes': len(act['scenes'])}
        actSpeechStart = totalSpeechNum
        actLineStart = totalLineNum
        for sceneNum in range(act['properties']['lengthScenes']):
            scene = {'plaintext': act['scenes'][sceneNum]}
            speakerForm = re.sub(form['speaker'], r'|speaker|\1|lines|', scene['plaintext'])
            scene['speeches'] = speakerForm.split('|speaker|')[1:]
            scene['properties'] = {'lengthSpeeches': len(scene['speeches']), 'startTotalLineNum': totalLineNum}
            totalSpeechNum += scene['properties']['lengthSpeeches']
            currentLineNum = 1
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
                    line = {'plaintext': speech['lines'][lineNum]}
                    line['properties'] = {'lineNum': currentLineNum, 'totalLineNum': totalLineNum}
                    currentLineNum += 1
                    totalLineNum += 1
                    speech['lines'][lineNum] = line
                    # figure out how to split into words when using punctuation and hyphens
                speech['properties']['endLineNum'] = currentLineNum-1
                speech['properties']['endTotalLineNum'] = totalLineNum-1
                scene['speeches'][speechNum] = speech
            scene['properties']['lengthLines'] = currentLineNum-1
            scene['properties']['endTotalLineNum'] = totalLineNum-1
            act['scenes'][sceneNum] = scene
        act['properties']['lengthLines'] = totalLineNum-actLineStart
        act['properties']['lengthSpeeches'] = totalSpeechNum-actSpeechStart
        text['acts'][actNum] = act
    text['properties']['lengthLines'] = totalLineNum
    text['properties']['lengthSpeeches'] = totalSpeechNum
    text['properties']['lengthScenes'] = totalSceneNum
    # generalize the format and include different ones so that you can make a recursive function for the for loops
    return text

text = openData('text')
data = textParse(text, form)

print data['acts'][1]['scenes'][0]['speeches'][13]
