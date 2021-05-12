# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:55:17 2021

@author: Lucas
"""

#%%
# list files in dataset directory
from create_corpus import list_directory

base_dir = "D:/Documentos/PFC-projeto/PFC/dataset/final/AtasCDINF/atasDOCX/"
files_docx = list_directory(base_dir)
print(files_docx)


#%%
# create corpus
from create_corpus import create_corpus
from create_corpus import clean_names

corpus = create_corpus(files_docx)
corpus = clean_names(corpus)

corpus_items = list(corpus.items())
print(corpus_items[:2])
print(len(corpus_items))

#%%

# filter off relevant corpus, based on the question, before feeding it into the model
from filter_corpus import filter_corpus

question_test = "Quando começou a Octogésima reunião do INF?"
relevant_corpus = filter_corpus(question_test, corpus)

relevant_corpus_items = list(relevant_corpus.items())
print(relevant_corpus_items)
print(len(relevant_corpus_items))

#%%

# create nlp model and pipeline
path_base = "pierreguillou/bert-base-cased-squad-v1.1-portuguese"

def createModel(model_path):
    # import transformers
    # don't forget to set device=0 so it runs on the GPU or -1 to run on CPU
    from transformers import pipeline
    nlp = pipeline("question-answering", model=model_path, device=0)
    print(nlp.device_placement)
    return nlp

nlp_base = createModel(path_base)

#%%

# process answer (args: question, model, corpus)
def answer_question(question, model, corpus):
    # filter the corpus, according to the question    
    corpus_items = filter_corpus(question, corpus).items()
    # feed the question and the corpus to the model
    results = {}
    for name, sample in corpus_items:
        result = model(question=question, context=sample)
        print(result)
        # append file name and answer to the question
        results[name] = result
    return results

# test question: "Quando começou a Octogésima reunião do INF?"
question = question_test
answers = answer_question(question, nlp_base, corpus)

#%%

question = "Quem presidiu a Centésima reunião?"
answers1 = answer_question(question, nlp_base, corpus)


#%%
# sort answers, and select best
# transform list into pandas dataframe (keys as labels and values as data)
import pandas as pd
def sort_answers(answers):
    # loop thru list of answers
    temp = []
    answers_list = answers.items()
    for name, answer in answers_list:
        # extract data from each dict
        data = list(answer.values())
        temp.append([name]+data)
        # append data to dataframe
    # sort dataframe on the score column
    # create dataframe
    # use keys in the first element as labels, plus the name of the file
    keys = list(answers.values())
    keys = keys[0].keys()
    columns = ['name'] + list(keys)
    # use temp as values
    df = pd.DataFrame(data=temp, columns=columns)#, sort='score')
    # sort values by the 'score' column
    df = df.sort_values('score', ascending=False)
    # return sorted dataframe
    return df

# print(pd.DataFrame(data=None, columns=list(answer[0].keys())))
sorted_answers = sort_answers(answers)
print(sorted_answers)
print("================")
sorted_answers1 = sort_answers(answers1)
print(sorted_answers1)

#%%

# display answers in order of relevance
# generator: receives list of answers as argument
def display_answers(answers):
    # loop thru answers
        # pick context:
            # crop 10 words around the cropped answer (use the start/end parameters as reference)
        # yield object with answer data:
            # return contains answer
            # return contains context around the answer
    pass

answers_displayer = display_answers(sorted_answers)

#%%
print(sorted_answers.iloc[0]['answer'])
print(sorted_answers.iloc[0])
# try implementing an interface
