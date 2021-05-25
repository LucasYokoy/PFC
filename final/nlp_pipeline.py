# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:55:17 2021

@author: Lucas
"""

#%%
# list files in dataset directory
if __name__ == '__main__':
    from create_corpus import list_directory
    # create corpus
    from create_corpus import create_corpus
else:
    from final.create_corpus import list_directory
    # create corpus
    from final.create_corpus import create_corpus

base_dir = "D:/Documentos/PFC-projeto/PFC/dataset/final/AtasCDINF/atasDOCX/"

#%%
# # create nlp model and pipeline
path_base = "pierreguillou/bert-base-cased-squad-v1.1-portuguese"

def createModel(model_path):
    # import transformers
    # don't forget to set device=0 so it runs on the GPU or -1 to run on CPU
    from transformers import pipeline
    nlp = pipeline("question-answering", model=model_path, device=0)
    print(nlp.device_placement)
    return nlp

#%%

# process answer (args: question, model, corpus)
def answer_question(question, model, corpus):
    # filter the corpus, according to the question    
    # corpus_items = filter_corpus(question, corpus).items()
    corpus_items = corpus.items()
    # feed the question and the corpus to the model
    results = {}
    for name, sample in corpus_items:
        result = model(question=question, context=sample)
        # append file name and answer to the question
        results[name] = result
    return results

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
    df = df.sort_values('score', ascending=False, ignore_index=True)
    # filter off answers with a score of less than 0.5
    df = df[df['score'] > 0.4]
    # return sorted dataframe
    return df

#%%

# extract context
def extract_context(answer, dataset):
    # pick start and end points
    answer_start = answer['start']
    answer_end = answer['end']
    # pick full text in dataset
    full_text = dataset[answer['name']]
    # attempt to exdtract 40 characters before and after the sentence (define in buffer)
    buffer = 100
    # add the buffer to the end, and subtract it from the begining
    answer_start -= buffer
    answer_end += buffer
    # detect if the buffered answer clips thru the begining or the end of the text
    # if the begining is now below zero, return slice [:end]
    if answer_start < 0:
        return full_text[:answer_end]
    # else if the end is now after the end of the text, return slice [begining:]
    elif answer_end >len(full_text):
        return full_text[answer_start:]
    # else, the answer doesn't clip through the begining or the end of the text, so return it as it is
    else:
        return full_text[answer_start:answer_end]
    
# display answers in order of relevance
# generator: receives list of answers as argument; yields one answer at a time
def display_answer(answers, corpus):
    # loop thru answers
    for answer in answers.iterrows():
        # pick context:
        answer = answer[1]
        context = extract_context(answer, corpus)
            # tell the name of the file
        # yield object with answer data:
        yield f"resposta: {answer['answer']}\nfonte:{answer['name']}\ncontexto:{context}\n"
            # return contains answer
            # return contains context around the answer

# answers_displayer = display_answers(sorted_answers)
# sorted_answers1 = sort_answers(answers)
def all_answers(answers_list, corpus):
    try:
        answer_gen = display_answer(answers_list, corpus)
        while True:
            print(next(answer_gen))
    except StopIteration:
        print("End of answers")

def all_answers1(answer_gen, corpus):
    try:
        # answer_gen = display_answer(answers_list, corpus)
        while True:
            print(next(answer_gen))
    except StopIteration:
        print("End of answers")

#%%
# evaluate a question on a single document, instead of the whole dataset
# create corpus outside of the function call
# files_docx = list_directory(base_dir)
# dataset = create_corpus(files_docx)

# create model outside function call
# model = createModel(path_base)

#%%
# display a single answer, with the proper format
def display_single_answer(answer, corpus, file_name):
    # use the same format as the display_answrs function, but for a single entry
    # pick context:
    # answer = answer[1]
    answer['name'] = file_name
    context = extract_context(answer, corpus)
        # tell the name of the file
    # return the chat formated answer
    return f"resposta: {answer['answer']}\nfonte:{answer['name']}\ncontexto:{context}\n"

# funcion gets a model, a corpus, a question and a document name as the argument
def answer_single_question(model, dataset, question, document):
    # fetch file from dataset body
    context = dataset[document]
    # apply the question to the document, using the model
    answer = model(question=question, context=context)
    # format answer with display_single_answer function
    # also return original answer object
    return answer, display_single_answer(answer, corpus=dataset, file_name=document)

#%%
# test single question answerer
# question = "Quem presidiu a 164a. reunião do CD do INF?"
# document = "ata 164-¬ reuni+úo ordin+íria 27-08-14.txt"
# answer= answer_single_question(model, dataset, question, document)
# print(answer)

#%%
# initialzie pipeline and dataset
# returns dataset (from base_dir), and pipeline function
# pipeline fucntion receives a question, and returns a generator of sorted answers
def initialize_pipeline():
    # create corpus
    files_docx = list_directory(base_dir)
    dataset = create_corpus(files_docx)
    # create model
    path_base = "pierreguillou/bert-base-cased-squad-v1.1-portuguese"
    model = createModel(path_base)
    # create answers generator
    def pipeline(question):
        # answer questions, and returns sorted list of answers
        answers_list = answer_question(question=question, model=model, corpus=dataset)
        # return generator that produces each answer
        answers_list = sort_answers(answers_list)
        return display_answer(answers_list, dataset)
    # return dataset and answers generator
    return dataset, pipeline

#%%
# pipeline to evaluate correct answer

# create answers evaluator (args:model, corpus, question, correct_answers)
# correct_answers must include the name of the document
def evaluate_answer(model, corpus, question, correct_answers):
    # call the answer_single_question function
    answer, _ = answer_single_question(model=model, 
                                    dataset=corpus,
                                    question=question,
                                    document=correct_answers['name'])
    # compare result to correct answer
    is_correct = (correct_answers['answer'] == answer['answer'] and
                  correct_answers['start'] == answer['start'] and
                  correct_answers['name'] == answer['name'])
    # return true if correct, and false otherwise
    # also return the given answer, and correct answer side by side
    return is_correct, answer
#%%
# evaluate correct answer's position

# create answers evaluator (args:model, corpus, question, correct_answers)
def find_answer_position(model, corpus, question, correct_answers):
    # call for the answer_question function
    answers_list = answer_question(question=question, model=model, corpus=corpus)
    # call for sort_answers function
    answers_list = sort_answers(answers_list)
    # find the correct answer on the list of answers, and fetch it's position
    correct_answer_index = answers_list.index[(answers_list['name']==correct_answers['name']) #&
                                              # (answers_list['start']==correct_answers['start']) &
                                              # (answers_list['answer']==correct_answers['answer'])
                                              ]
    # if the correct answer isn't found, return -1
    try:
        correct_answer_index = correct_answer_index[0] 
    except IndexError:
        correct_answer_index=-1
    # return the position of the correct answer on the list
    # also return the list
    return correct_answer_index, answers_list

#%%
# # create corpus and model externally

# files_docx = list_directory(base_dir)
# dataset = create_corpus(files_docx)
# model = createModel(path_base)
# #%%
# # evaluate the question
# question = "Quem presidiu a 164a. reunião do CD do INF?"
# document = "ata 164-¬ reuni+úo ordin+íria 27-08-14.txt"
# correct_answer = { 'name': "ata 164-¬ reuni+úo ordin+íria 27-08-14.txt",
#                   'answer': "professor Plínio de Sá Leitão Júnior",
#                   'start':313,
#                   'end':349,
#                   }
# answer, chat_answer = answer_single_question(model, dataset, question, document)
# print(chat_answer)
# print(answer)
#%%
# is_correct, answer = evaluate_answer(model=model,
#                                      corpus=dataset,
#                                      question=question,
#                                      correct_answers=correct_answer)
# print(is_correct)
# print(answer)
#%%
# answer_index, answers_list = find_answer_position(model=model,
#                                                   corpus=dataset,
#                                                   question=question,
#                                                   correct_answers=correct_answer)

# print(answer_index)
# print(answers_list.iloc[answer_index])
# print(answers_list)
