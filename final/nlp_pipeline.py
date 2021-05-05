# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:55:17 2021

@author: Lucas
"""

# Get path to all files in all folders in /dataset/final
# On first version, do only /dataset/final/AtasCDINF
# return list with paths to files
import os
# dataset_basedir = "D:/Documentos/PFC-projeto"
# raw_dir = dataset_basedir + "/dataset/final/AtasCDINF/atasDOCX/"
base_dir = "D:/Documentos/PFC-projeto/PFC/dataset/final/AtasCDINF/atasDOCX/"
def listDirectory(base_dir):
    files = os.listdir(base_dir)
    files = [base_dir + file_path for file_path in files]
    return files

files_docx = listDirectory(base_dir)
print(files_docx)

#%%

# create corpus
# function that opens each file:
def openFile(path):
    # open file path
    my_file = open(path, mode='r', encoding='utf-8')
    # for each line in the file
    file_var = ""
    for line in my_file:
        # append line to variable
        file_var += line
    # return variable
    return file_var

# open all documents and append them to a list
def createCorpus(file_list):
    # output is initially an empty string
    output = []
    # loop thru list of file paths
    for filename in file_list:
        # open file (read mode)
        file = openFile(filename)
        # append that to output
        output.append(file)
    return output

corpus = createCorpus(files_docx)
print(corpus)
print(len(corpus))

#%%

# create nlp model and pipeline (one with base and one with large)
path_base = "pierreguillou/bert-base-cased-squad-v1.1-portuguese"
# path_large = "pierreguillou/bert-large-cased-squad-v1.1-portuguese"
def createModel(model_path):
    # import transformers
    # don't forget to set device=0 so it runs on the GPU or -1 to run on CPU
    from transformers import pipeline
    nlp = pipeline("question-answering", model=model_path, device=0)
    print(nlp.device_placement)
    return nlp

nlp_base = createModel(path_base)
# nlp_large = createModel(path_large)

#%%

# process answer (args: question, model, corpus)
def answer_question(question, model, corpus):
    # feed the question and the corpus to the model
    results = []
    for text in corpus:
        result = model(question=question, context=text)
        print(result)
        results.append(result)
    return results
    # pick context:
        # crop 10 words around the cropped answer (use the start/end parameters as reference)
    # return object with answer data:
        # return contains answer
        # return contains context around the answer

question = "Quem presidiu a octagésima reunião do INF?"
answer = answer_question(question, nlp_base, corpus)
print(answer)
#%%
# sort answers, and select best
# transform list into pandas dataframe (keys as labels and values as data)
import pandas as pd
def sort_answers(answers_list):
    # loop thru list of answers
    temp = []
    for answer in answers_list:
        # extract data from each dict
        data = list(answer.values())
        temp.append(data)
        # append data to dataframe
    # sort dataframe on the score column
    # create dataframe
    # use keys in the first element as labels
    columns = list(answers_list[0].keys())
    # use temp as values
    df = pd.DataFrame(data=temp, columns=columns)#, sort='score')
    # sort values by the 'score' column
    df = df.sort_values('score', ascending=False)
    # return sorted dataframe
    return df

# print(pd.DataFrame(data=None, columns=list(answer[0].keys())))
sorted_answers = sort_answers(answer)
print(sorted_answers)
#%%

print(sorted_answers.iloc[0]['answer'])
# try implementing an interface
