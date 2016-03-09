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
    'speaker': r'(\w+):\n',
    'line': r'([^\n]+)\n'
}

def openData(doc):
    text = open(doc, 'r')
    text = text.read()
    return text


def textParse(text, form):
    plaintext = text
    speakers = {}
    #make a parser to separate the stage instructions from stats
    text = {
        'lengthActs': 0,
        'lengthScenes': 0,
        'lengthSpeeches': 0,
        'lengthLines': 0,
        'lengthWords': 0,
        'lengthChars': 0
    }

    acts = re.split(form['act'], plaintext)[1:]

    for act in acts:
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
            speakerForm = re.sub(form['speaker'], r'|speaker|\1|lines|', scene)
            speeches = speakerForm.split('|speaker|')[1:]

            scene = {
                'lengthSpeeches': 0,
                'lengthLines': 0,
                'lengthWords': 0,
                'lengthChars': 0
                # 'startLineTotal': text['properties']['lengthLines']
            }

            for speech in speeches:
                speakerAndLines = speech.split('|lines|')
                lines = speakerAndLines[1].split('\n')[:-1]

                speech = {
                    'speaker': speakerAndLines[0],
                    'words': {},
                    'chars': {},
                    'lengthLines': 0,
                    'lengthWords': 0,
                    'lengthChars': 0
                }

                for line in lines:

                    words = re.sub('[^[a-zA-z-\']]', '', line).lower()
                    words = words.split(' ')
                    for word in words:
                        if not word in speech['words']:
                            speech['words'][word] = 1
                        else:
                            speech['words'][word] += 1

                    chars = re.sub('[a-zA-z]', '', line)
                    for char in chars:
                        if not char in speech['chars']:
                            speech['chars'][char] = 1
                        else:
                            speech['chars'][char] += 1

                    line = {
                        'lineNum': scene['lengthLines'],
                        'lengthWords': len(words),
                        'lengthChars': len(line)
                    }


                    speech['lengthLines'] += 1
                    speech['lengthWords'] += line['lengthWords']
                    speech['lengthChars'] += line['lengthChars']
                    speech[speech['lengthLines']] = line

                scene['lengthSpeeches'] += 1
                scene['lengthLines'] += speech['lengthLines']
                scene['lengthWords'] += speech['lengthWords']
                scene['lengthChars'] += speech['lengthChars']
                scene[scene['lengthSpeeches']] = speech

            act['lengthScenes'] += 1
            act['lengthSpeeches'] += scene['lengthSpeeches']
            act['lengthLines'] += scene['lengthLines']
            act['lengthWords'] += scene['lengthWords']
            act['lengthChars'] += scene['lengthChars']
            act[act['lengthScenes']] = scene

        text['lengthActs'] += 1
        text['lengthScenes'] += act['lengthScenes']
        text['lengthSpeeches'] += act['lengthSpeeches']
        text['lengthLines'] += act['lengthLines']
        text['lengthWords'] += act['lengthWords']
        text['lengthChars'] += act['lengthChars']
        text[text['lengthActs']] = act
    # generalize the format and include different ones so that you can make a recursive function for the for loops
    return text

text = openData('text')
text = textParse(text, form)

# print text
