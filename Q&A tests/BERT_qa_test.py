#!/usr/bin/env python
# coding: utf-8

# In[1]:


from transformers import BertModel
# model_path = 'neuralmind/bert-base-portuguese-cased'
model_path = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
model = BertModel.from_pretrained(model_path)


# In[2]:


from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained(model_path)


# In[4]:


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

corpus = openFile(".\\docs\\txt\\80a Reuni+úo.txt")#"D:\\Documentos\\Tutorials\\MachineLearning\\tensorflow\\docs\\txt\\80a Reuni+úo.txt")
print(corpus)
print(len(corpus))
#%%
# corpus = corpus[]

# In[5]:


# create a questions and answers pipeline for the model and t he questions/answers
import torch
def answer_question(question, answer_text):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.
    '''
    # ======== Tokenize ========
    # Apply the tokenizer to the input text, treating them as a text-pair.
    input_ids = tokenizer.encode(question, answer_text)

    # Report how long the input sequence is.
    print('Query has {:,} tokens.\n'.format(len(input_ids)))

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    # ======== Evaluate ========
    # Run our example through the model.
    outputs = model(torch.tensor([input_ids]), # The tokens representing our input text.
                    token_type_ids=torch.tensor([segment_ids]), # The segment IDs to differentiate question from answer_text
                    return_dict=True) 

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    answer = tokens[answer_start]

    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):
        
        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        
        # Otherwise, add a space then the token.
        else:
            answer += ' ' + tokens[i]

    return 'Answer: "' + answer + '"'


# In[6]:


# format corpus for the model
import textwrap

# Wrap text to 80 characters.
wrapper = textwrap.TextWrapper(width=80)

# f_corpus = wrapper.fill(corpus)
# f_corpus = f_corpus[:1000]
f_corpus = corpus[:1000]
print(f_corpus)
print(len(f_corpus))


# In[7]:

# run question on cf_corpus
question = "Quando ocorreu a octagésima reunião do conselho diretor do instituto de informática?"
print(answer_question(question, f_corpus))

#%%
question = "Onde foi descoberta a Covid-19?"
f_corpus = "A pandemia de COVID-19, também conhecida como pandemia de coronavírus, é uma pandemia em curso de COVID-19, uma doença respiratória aguda causada pelo coronavírus da síndrome respiratória aguda grave 2 (SARS-CoV-2). A doença foi identificada pela primeira vez em Wuhan, na província de Hubei, República Popular da China, em 1 de dezembro de 2019, mas o primeiro caso foi reportado em 31 de dezembro do mesmo ano."

print(answer_question(question, f_corpus))