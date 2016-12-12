SylliGram implements unsupervised learning for automatic syllabification. It uses PyAdaGram, an AdaptorGrammar software developed by https://github.com/kzhai. An AdaptorGrammar is a subset of Probabilistic Context-free Grammars (PCFGs) which uses a Pitman-Yor distribution over distributions to adjust the probability of a subtree expansion based on its frequency in the data. SylliGram establishes a pipeline for a user to syllabify a list of words. To use the software, the user must provide the following:

1. a list of words to be syllabified. This should be a text file with one word on each line, where each phone of the word is separated by spaces.
2. a "segment file". This is a file with 2-3 lines of comma-separated values, where the first line is a list of syllabic segments in the list of words, the second is a list of non-syllabic segments, and the third (optional) is a list of semi-syllabic segments (i.e. segments that can act as either syllabic or non-syllabic depending on the context, such as /l/ or /n/ in English). If any phones are found in the corpus and not in the segment file, the program will alert the user

The program also requires various Python dependencies, including numpy, scipy, and nltk. These should be installed **for Python 2**. The easiest way to do this is to install Python 2, and then use the `pip2 install` command. 

Once this is done, SylliGram is run by using the following command:
    `python main.py <SEGMENT_FILE> <LIST_OF_WORDS> <NAME_FOR_GRAMMAR>`
where the user may choose any desired name for the grammar. The output will be a file called "syllabified" written to the same directory that contained the list of words. 

In ./demo/, you can find 2500 sample words in French, from the Lexique corpus, along with a sample segment file, and a properly syllabified test document. To run these 2500 words, you can use the following command (assuming you are in the parent directory):
    `python2 main.py demo/demo_segfile demo/french_2500 demo/french_grammar`

This will take ~10 minutes, depending on your machine. To compare the produced file against the syllabified corpus (assuming you are in the parent directory) input:
    `python bin/compare.py demo/syllabified demo/lexique_syllabified`