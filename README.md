# Shakespeare Analysis
A parser and analyzer to get numerical data from texts of the Shakespeare format.

Heavily influenced and borrowed from:
Open Source Shakespeare:  www.opensourceshakespeare.org/

#### Overview:
This program takes in a play and it's format, parses it into acts, scenes, speakers, speeches, and lines, and labels each with information (e.g. number of words). Then, it will be able to quickly print any part of the play (sorted in various ways) and compare the information of characters and plays, and much, much more (to be implemented).

#### Data Structure:
The main text splits into many layered subsets:

    set = {text, subsets, analysis}
    set[subsets] = [subset1, subset2, ... ]
    subset1 = {text, subsets, analysis}
  
  where text is the plaintext, subsets are a smaller set like scenes in an act, and analysis is where we get calculated variables which can be then processed to produce more complex analysis
  
  analysis should include: actNum, sceneNum, speechNum, lineNum, wordNum, charNum, speakerNum, and more
    
Additionally, there will be a list of speakers

    speakers['speaker'] = {text, speeches, analysis}

#### Features that Should Exist:

