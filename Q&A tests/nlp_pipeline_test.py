# -*- coding: utf-8 -*-
"""
Created on Mon May  3 15:02:36 2021

@author: Lucas
"""

# import transformers
from transformers import pipeline

# source: https://pt.wikipedia.org/wiki/Pandemia_de_COVID-19
context = r"""
A pandemia de COVID-19, também conhecida como pandemia de coronavírus, é uma pandemia em curso de COVID-19, 
uma doença respiratória aguda causada pelo coronavírus da síndrome respiratória aguda grave 2 (SARS-CoV-2). 
A doença foi identificada pela primeira vez em Wuhan, na província de Hubei, República Popular da China, 
em 1 de dezembro de 2019, mas o primeiro caso foi reportado em 31 de dezembro do mesmo ano. 
Acredita-se que o vírus tenha uma origem zoonótica, porque os primeiros casos confirmados 
tinham principalmente ligações ao Mercado Atacadista de Frutos do Mar de Huanan, que também vendia animais vivos. 
Em 11 de março de 2020, a Organização Mundial da Saúde declarou o surto uma pandemia. Até 8 de fevereiro de 2021, 
pelo menos 105 743 102 casos da doença foram confirmados em pelo menos 191 países e territórios, 
com cerca de 2 308 943 mortes e 58 851 440 pessoas curadas.
"""

model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nlp = pipeline("question-answering", model=model_name)

question = "Quando começou a pandemia de Covid-19 no mundo?"

result = nlp(question=question, context=context)

print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")

# Answer: '1 de dezembro de 2019 score: 0.713, start: 328, end: 349
#%%
# open corpus
def openFile(path):
    # open file path
    my_file = open(path, encoding='utf-8')
    # for each line in the file
    file_var = ""
    for line in my_file:
        # append line to variable
        file_var += line
    # return variable
    return file_var

corpus = openFile(".\\docs\\txt\\80a Reuni+úo.txt")
#%%
question="Quando começou a octagésima reunião?"
result = nlp(question=question, context=corpus)
print(result)