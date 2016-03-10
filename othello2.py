# properties = {actNum, sceneNum, speechNum, lineNum, wordNum, charNum, speakerNum}
# fix line spacing with tabs
# get rid of plaintext
# make array dictionary combo: act = {1: scene1, 2: scene2 ... 'properties': properties}
import re
# Make print function to replace the 99.99% of storage used by deleting plaintext for everything but characters and speakers
# change variables of scene['properties']['lengthLines'] and such to changing variables within the dictionary
form = {
    'act': r'Act \d+:\n',
    'scene': r'Scene \d+:\n',
    'speaker': r'\n(\w+):\n',
    'line': r'([^\n]+)\n'
}

def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text

# trade off between code organization+readability and efficiency (function calls)
def addDicts(original, addition):
    keys = original.keys();
    for key in addition.keys():
        if key in keys:
            original[key] += addition[key]
        else:
            original[key] = addition[key]
    return original

def addToDict(original, addition):
    if addition in original.keys():
            original[addition] += 1
    else:
            original[addition] = 1

def textParse(text, form):
    plaintext = text
    speakers = {}
    #make a parser to separate the stage instructions from stats
    text = {
        'lengthSpeakers': 0,
        'lengthActs': 0,
        'lengthScenes': 0,
        'lengthSpeeches': 0,
        'lengthLines': 0,
        'lengthWords': 0,
        'lengthChars': 0
    }

    acts = re.split(form['act'], plaintext)[1:]

    for act in acts:
        text['lengthActs'] += 1

        scenes = re.split(form['scene'], act)[1:]

        act = {
            # 'actNum': text['lengthActs']
            'lengthScenes': 0,
            'lengthSpeeches': 0,
            'lengthLines': 0,
            'lengthWords': 0,
            'lengthChars': 0
            # 'startLineTotal': text['lengthLines'],
            # 'startSpeechTotal': text['lengthSpeeches']
        }

        for scene in scenes:
            act['lengthScenes'] += 1
            if text['lengthActs']==1 and act['lengthScenes']==3:
                print scene
            speakerForm = re.sub(form['speaker'], r'|speaker|\1|lines|', '\n' + scene)
            speeches = speakerForm.split('|speaker|')[1:]

            scene = {
                'lengthSpeeches': 0,
                'lengthLines': 0,
                'lengthWords': 0,
                'lengthChars': 0
                # 'startLineTotal': text['properties']['lengthLines']
            }

            for speech in speeches:
                scene['lengthSpeeches'] += 1

                speakerAndLines = speech.split('|lines|')
                # print speakerAndLines
                lines = speakerAndLines[1].split('\n') #[:-1]

                speech = {
                    'speaker': speakerAndLines[0],
                    'words': {},
                    'chars': {},
                    'lengthLines': 0,
                    'lengthWords': 0,
                    'lengthChars': 0
                }

                for line in lines:
                    speech['lengthLines'] += 1

                    words = re.sub('[^[a-zA-z-\']]', '', line).lower()
                    words = words.split(' ')
                    chars = re.sub('[a-zA-z]', '', line)

                    line = {
                        'lineNum': scene['lengthLines'],
                        'lengthWords': 0,
                        'lengthChars': len(line)
                    }

                    for word in words:
                        line['lengthWords'] += 1
                        if word in speech['words']:
                            speech['words'][word] += 1
                        else:
                            speech['words'][word] = 1

                    for char in chars:
                        if not char in speech['chars']:
                            speech['chars'][char] = 1
                        else:
                            speech['chars'][char] += 1

                    speech['lengthWords'] += line['lengthWords']
                    speech['lengthChars'] += line['lengthChars']
                    speech[speech['lengthLines']] = line

                if not speech['speaker'] in speakers.keys():
                    speakers[speech['speaker']] = {text['lengthActs']: {act['lengthScenes']: [scene['lengthSpeeches']]}}
                elif not text['lengthActs'] in speakers[speech['speaker']].keys():
                    speakers[speech['speaker']][text['lengthActs']] = {act['lengthScenes']: [scene['lengthSpeeches']]}
                elif not act['lengthScenes'] in speakers[speech['speaker']][text['lengthActs']].keys():
                    speakers[speech['speaker']][text['lengthActs']][act['lengthScenes']] = [scene['lengthSpeeches']]
                else:
                    speakers[speech['speaker']][text['lengthActs']][act['lengthScenes']] += [scene['lengthSpeeches']]

                scene['lengthLines'] += speech['lengthLines']
                scene['lengthWords'] += speech['lengthWords']
                scene['lengthChars'] += speech['lengthChars']
                scene[scene['lengthSpeeches']] = speech

            act['lengthSpeeches'] += scene['lengthSpeeches']
            act['lengthLines'] += scene['lengthLines']
            act['lengthWords'] += scene['lengthWords']
            act['lengthChars'] += scene['lengthChars']
            act[act['lengthScenes']] = scene

        text['lengthScenes'] += act['lengthScenes']
        text['lengthSpeeches'] += act['lengthSpeeches']
        text['lengthLines'] += act['lengthLines']
        text['lengthWords'] += act['lengthWords']
        text['lengthChars'] += act['lengthChars']
        text[text['lengthActs']] = act
        text['speakers'] = speakers
    # generalize the format and include different ones so that you can make a recursive function for the for loops
    return text

plaintext = openData('text')
text = textParse(plaintext, form)

# speakers mix with other words at the end
# some parsing problems
print text['speakers'].keys()
