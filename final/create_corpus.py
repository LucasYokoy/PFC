# -*- coding: utf-8 -*-
"""
Created on Fri May  7 12:59:34 2021

@author: Lucas

This section pertains the opening of the files contained in the corpus,
and the final preprocessing of the corpus
"""
#%%
# Get path to all files in all folders in /dataset/final
# On first version, do only /dataset/final/AtasCDINF
# return list with paths to files
import os
def list_directory(base_dir):
    files = os.listdir(base_dir)
    files = [base_dir + file_path for file_path in files]
    return files

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

#%%
# open all documents and append them to a list
def create_corpus(file_list):
    # output is initially an empty dictionary of name-file pairs
    output = {}
    # loop thru list of file paths
    for filename in file_list:
        # open file (read mode)
        file = openFile(filename)
        # extract file name (everything after the last '/')
        name = filename.rsplit('/', 1)[1]
        # append file name and content to output
        output[name] = file
    # clean list of names in the end, using tabs
    # loop thru list of files
    file_list = output.items()
    output = {}
    for file_name, file_content in file_list:
        # split file in sections by '.'
        sectioned_file = file_content.split('.')
        # loop thru sections in file, starting from the last one
        for section in reversed(sectioned_file):
            # count how many '\t' characters show up in that section.
            # if there are too many:
            if '\t' in section: #section.count('\t') > 0:
                # delete section
                sectioned_file.pop()
                # continue to next section
            # else:
            else:
                # rejoin sections
                output[file_name] = '.'.join(sectioned_file) + '.'
                # escape loop and continue to the next file
                break
            # if reached the end of the file, raise exception
            # that means the whole file has been deleted
            # raise ValueError(f"All sections have been deleted in file {file_index}.")
    return output

 #%%
# import re
# clean list of names in the end, using capital letters
# def clean_names_capitals(file_list):
    # loop thru list of files
        # split file in sections by '.'
        # loop thru sections, starting in the last one

            # count the number of words in each section:
            # split sections by ' '
            # count the lenght of the split section
            
            # count the number of possible proper names in each section:
            # count how many words satisfy the proper name regex r'[A-ZÁÉÍÓÔÊÃÕ][a-zçáéíóôêãõ\.]+'
        
            # compare the two
            # if most words in that section follow the proper name regex
                # delete section: section.pop()
                # continue to the next section
            # else, rejoin all sections, break out of the loop, and continue to the next file
                # ' '.join(split_section)
    # pass
