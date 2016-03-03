import re
# [0 lineNum, 1 'Speaker', 2 'Text', 3 actNum, 4 SceneNum, 5 charNum, 6 wordNum],
# [3676, 'othello', 'O villain!\n', ' O FLN ', ' o villain ', 5, 2, 11, 2],
def getData():
    def openData(doc):
        text=open(doc,'r')
        text=text.read()
        text=text.split('\n')
        text.pop()
        return text
    text=openData('text')

    def varDec():
        global sortedText, chars
        sortedText={}
        chars={}
    varDec()

    currentAct=0
    currentScene=0

    for i in range(len(text)):
        speech=text[i]
        def speechFormat(speech):
            speech=speech.split('|')
            # speech=[int(speech[0]), speech[1], speech[2], int(speech[5]), int(speech[6]), int(speech[7]), int(speech[8])] #make into hashmap
            speech[2]=re.sub('\[p\]','\n',speech[2])
            print speech[2]
            speech={'totalLineNum': int(speech[0]), 'speaker': speech[1], 'text': speech[2], 'act': int(speech[5]), 'scene': int(speech[6]), 'charNum': int(speech[7]), 'wordNum': int(speech[8])}
            return speech
        speech=speechFormat(speech)
        text[i]=speech
        # totalLineNum = speech['totalLineNum']
        speaker = speech['speaker']
        # text = speech['text']
        act = speech['act']
        scene = speech['scene']
        # charNum = speech['charNum']
        # wordNum = speech['wordNum']

        if not speaker in chars:
            chars[speaker]={act: {scene: []}}

        if act!=currentAct:
            currentAct=act
            sortedText[act]={}
            for char in chars.keys():
                chars[char][act]={scene: []}

        if scene!=currentScene:
            currentScene=scene
            sortedText[act][scene]=[]
            for char in chars.keys():
                chars[char][act][scene]=[]

        chars[speaker][act][scene].append({'totalLineNum': speech['totalLineNum'], 'text': speech['text'], 'charNum': speech['charNum'], 'wordNum': speech['wordNum']})
        sortedText[act][scene].append({'totalLineNum': speech['totalLineNum'], 'speaker': speaker, 'text': speech['text'], 'charNum': speech['charNum'], 'wordNum': speech['wordNum']})
    return {'text':text, 'chars':chars}
data = getData()
print data['chars'].keys()
# text= data['text']
# chars = data['chars']
# print chars['iago'][2][1]
