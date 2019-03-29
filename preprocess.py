# Preprocess a play from Gutenberg
# https://www.gutenberg.org/files/1771/1771.txt

import re

def preprocess_text(text):
    # Remove stuff before the play starts and after it ends
    beginning = re.search("ACT 1. SCENE I.", text).start()
    end = re.search("THE END", text).start()
    text = text[beginning:end] + '|end|'

    # Remove copyright stuff
    text = re.sub("<<.+?>>", "", text, flags=re.DOTALL)

    # text = re.sub(r'\n  [ ]+([A-Z1-9 ]+)\. ', r'\n|speaker|\1|lines|    ', text) ACT 

    # Label acts
    text = re.sub(r'ACT \w+\. ', '|act|', text)
    # Label scenes
    text = re.sub(r'SCENE (\w+)\.\n', '|scene|', text)
    # Label speakers
    text = re.sub(r'\n  [ ]*([A-Z1-9 &]+)\. ', r'\n|speaker|\1|lines|    ', text)
    # Label stage directions not labeled with brackets
    text = re.sub(r'([^\s|]|\n    )(   [ ]*)([^\[ ].*)((\n    [ ]+.*)*)\n(\||    \w)', r'\1\2[\3\4]\n\6', text)
    text = re.sub(r'\|scene\|(.*?)\n\|speaker\|', r'|scene|[\1]\n|speaker|', text, flags=re.DOTALL)

    # Remove stage directions (temporary)
    text = re.sub(r'\[.*?(\[.*?\].*?)?\]', '', text, flags=re.DOTALL)
    # Remove end marker
    text = re.sub(r'\|end\|', '', text)
    # Remove whitespace
    text = re.sub(r'\s+\n', '\n', text)
    text = re.sub(r'    ', '', text)
    text = re.sub(r' +', ' ', text)

    # print(text[:100], text[-100:])
    return text

def preprocess(original, target):
    text_file = open(original, 'r')
    text = text_file.read() 

    processed = preprocess_text(text)

    text_file.close()
    save_file = open(target, 'w')
    save_file.write(processed)

if __name__ == "__main__":
    original = "titus.txt"
    target = "processed_titus.txt"

    play = preprocess(original, target)
