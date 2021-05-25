# -*- coding: utf-8 -*-
"""
Created on Fri May  7 12:49:15 2021

@author: Lucas

This section pertains the filtering off of the corpus.

Here, each file on the corpus will be evaluated according to the question, and
included in the filtered version of the corpus if they are thought to be relevant.

Initially, the only criteria will be the presence of capitalized words in the text,
that also happen in the corpus.

words considered:
    any capitalized word
words ignored:
    the first word on the question
    the word INF, because it shows up everywhere

The above system can be improved upon. Ideally, a machine learning algorithm
can be trained to read the text, compare it to the question and give a grade on
whether or not the text is relevant.
"""

#%%
# only the documents that contain the capitalized words are shown.
import re
def filter_corpus(question, corpus):
    # decapitalize the first word in the question (it's always capitalized for grammatical reasons)
    temp = question.split(' ')
    temp[0] = temp[0].lower()
    question = ' '.join(temp)

    # search for all other capitalized words with findall regex r'[A-ZÁÉÍÓÂÔÊÃÕ].*'
    # lower case the words to facilitate comparison
    # also remove punctuation
    capitalized_words = re.findall(r'[A-Z][^ ]*', question)
    capitalized_words = [word.lower().replace('.','').replace(',','') for word in capitalized_words]
    capitalized_words = [word.replace('?','').replace('!','').replace(';','') for word in capitalized_words]
    
    # also ignore the word INF, if it shows up in the text (it shows up everywhere)
    capitalized_words = [word for word in capitalized_words if word != 'inf']
    
    # include numbers
    capitalized_words += re.findall(r'[0-9]*', question)
    
    # loop thru texts in corpus
    output = {}
    corpus_items = corpus.items()
    for name, text in corpus_items:
        # lowercase the text, to facilitate comparison
        # if one of the capitalized words is in the corpus, add it to the return corpus
        lowercase_text = text.lower()
        if any(word in lowercase_text for word in capitalized_words):
            output[name] = text
    # if the length of the filtered corpus is 0, filter nothing
    if len(output.items()) == 0:
        return corpus
    return output