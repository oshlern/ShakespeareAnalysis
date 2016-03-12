# fix line spacing with tabs
# make a parser to separate the stage instructions from stats
# char count w/ speakers?
# fix general char count (not chars)
import re
form = {
    'act': r'Act \d+:\n',
    'scene': r'Scene \d+:\n',
    'speaker': r'\n(\w+):\n',
    'line': r'([^\n]+)\n'
}
doWords = False
doChars = False
doSpeakers = True


def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text
def saveData(doc, data):
    output = open(doc,"w")
    output.write(data)

# trade off between code organization+readability and efficiency (function calls)
# add a possible remove
def addDicts(original, addition, remove):
    if 'subsets' in original:
        original['subsets'] += [addition]
    for key in addition:
        if key != 'subsets' and key != remove:
            if key in original:
                if isinstance(original[key], dict) and isinstance(addition[key], dict):
                    original[key] = addDicts(original[key], addition[key], 'NULL')
                # elif isinstance(original[key], int) and isinstance(addition[key], int): #or array
                else:
                    original[key] += addition[key]
            else:
                original[key] = addition[key]
    return original

def addToDict(original, addition):
    if addition in original.keys():
            original[addition] += 1
    else:
            original[addition] = 1

def speakerInfo(speaker):
    properties = {'lengthActs': 0}
    for actNum in speaker.keys():
        act = {'lengthScenes': 0}
        for sceneNum in speaker[actNum].keys():
            scene = {'lengthSpeeches': 0}
            for speechNum in speaker[actNum][sceneNum]:
                scene = addDicts(scene, text[actNum][sceneNum][speechNum], 'NULL')
                scene['lengthSpeeches'] += 1
            act = addDicts(act,scene, 'NULL')
            act['lengthScenes'] += 1
        properties = addDicts(properties, act, 'NULL')
        properties['lengthActs'] += 1
    speaker = addDicts(speaker, properties, 'NULL')
    return speaker

def textParse(text, form):
    plaintext = text
    acts = re.split(form['act'], plaintext)[1:]
    text = {'lengthActs': 0, 'subsets': []}
    for act in acts:
        text['lengthActs'] += 1
        scenes = re.split(form['scene'], act)[1:]
        act = {'lengthScenes': 0, 'subsets': []}
        for scene in scenes:
            act['lengthScenes'] += 1
            speakerForm = re.sub(form['speaker'], r'|speaker|\1|lines|', '\n' + scene)
            speeches = speakerForm.split('|speaker|')[1:]
            scene = {'lengthSpeeches': 0, 'lengthLines': 0, 'subsets': []}
            if doSpeakers:
                scene['speakers'] = {}
                scene['lengthSpeakers'] = 0
            for speech in speeches:
                scene['lengthSpeeches'] += 1
                speakerAndLines = speech.split('|lines|')
                speech = {'lengthLines': 0, 'subsets': []}
                if doWords: speech['words'] = {}
                if doChars: speech['chars'] = {}
                speech['speaker'] = speakerAndLines[0]
                lines = speakerAndLines[1].split('\n') #[:-1]

                if doSpeakers:
                    if not speech['speaker'] in scene['speakers']: #fix to be speakers in speech
                        scene['lengthSpeakers'] += 1
                        scene['speakers'][speech['speaker']] = {}
                    if not text['lengthActs'] in scene['speakers'][speech['speaker']]:
                        scene['speakers'][speech['speaker']][text['lengthActs']] = {}
                    if not act['lengthScenes'] in scene['speakers'][speech['speaker']][text['lengthActs']]:
                        scene['speakers'][speech['speaker']][text['lengthActs']][act['lengthScenes']] = []
                    scene['speakers'][speech['speaker']][text['lengthActs']][act['lengthScenes']] += [scene['lengthSpeeches']]

                for line in lines:
                    speech['lengthLines'] += 1
                    words = re.sub('[^a-zA-z-\' ]', '', line)
                    words = words.lower()
                    words = words.split(' ')
                    chars = re.sub('[a-zA-z]', '', line)
                    line = {
                        'lineNum': scene['lengthLines'] + speech['lengthLines'],
                        'lengthWords': len(words),
                        'lengthChars': len(line)
                    }
                    if doWords:
                        for word in words:
                            if not word in speech['words']:
                                speech['words'][word] = 0
                            speech['words'][word] += 1
                    if doChars:
                        for char in chars:
                            if not char in speech['chars']:
                                speech['chars'][char] = 0
                            speech['chars'][char] += 1

                    speech = addDicts(speech, line, 'lineNum')
                scene = addDicts(scene, speech, 'speaker')
            act = addDicts(act, scene, 'NULL')
        text = addDicts(text, act, 'NULL')
    return text
    # generalize the format and include different ones so that you can make a recursive function for the for loops


plaintext = openData('text')
text = textParse(plaintext, form)
# print text.pop('subsets', None)
# print text.pop('speakers', None)
print len(text['speakers'])

# number of times a speaker is mentioned by name
# number of distinct words used by characters (vocabulary) (per number of total words)
# for i in len(format), split and parse text in the existing for loops !!!!
