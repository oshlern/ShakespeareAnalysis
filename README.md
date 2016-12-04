# Bot
Chat Bot

Influenced by:
Open Source Shakespeare (www.opensourceshakespeare.org)

#### Overview:


#### Data Structure:
Fix:
The main text splits into many layered subsets:

    set = {subsets, analysis, analysis2, ... }
    set[subsets] = [subset1, subset2, ... ]
    subset1 = {subsets, analysis, analysis2, ... }

  where subsets are a smaller set like scenes in an act, and analysis is where we get calculated variables which can be then processed to produce more complex analysis

  analysis should include: actNum, sceneNum, speechNum, lineNum, wordNum, charNum, speakerNum, and more

    Text = {'plaintext', 'acts', 'analysis', 'speakers']
      acts = [{'plaintext', 'scenes', 'analysis', 'speakers'}]
        scenes = [{plaintext, speeches, analysis, speakers, lines}]
          speeches = [{plaintext, speech, analysis, speaker}]
            speech = {plaintext, lines, analysis,} //this is the part of the speech that is not the speaker. maybe add 'speaker property
              lines = [{plaintext,
Additionally, there will be a list of speakers
    change analysis to properties

    speakers['speaker'] = {text, speeches, analysis}

#### Features that Should Exist:
