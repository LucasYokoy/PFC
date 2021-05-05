# -*- coding: utf-8 -*-
"""
Created on Wed May  5 10:48:50 2021

@author: Lucas
"""

# In[ ]
# Get path to all files in all folders in /dataset/raw
# On first version, do only /dataset/raw/AtasCDINF
# return list with paths to files
import os
dataset_basedir = "D:\\Documentos\\PFC-projeto\\dataset"
rawPDF_dir = dataset_basedir + "\\raw\\AtasCDINF\\atasPDF\\"
def listDirectory(raw_dir):
    files = os.listdir(raw_dir)
    files = [raw_dir + file_path for file_path in files]
    return files

files_pdf = listDirectory(rawPDF_dir)
# In[ ]
import docx
def extractDocxData(path):
    """Extract text from word documents"""
    # doc = docx2txt.process(path)
    # return doc

    doc = docx.Document(path)
    output = ""
    for paragraph in doc.paragraphs:
        output = output + "\n" + paragraph.text
    return output

import fitz
import pytesseract
def extractPDFData(path):
    """Extract all data from a pdf (from both image and text)"""
    # Open file
    file = fitz.open(path)
    pages = file.pages()
    output = ""
    # cycle thru all pages
    for pageNumber, page in enumerate(pages):
        images = page.getImageList()
        # extract text from the images on the page
        for imgNumber, img in enumerate(images):
            xref = img[0]
            pix = fitz.Pixmap(file,xref)
            if pix.n > 4:
                pix = fitx.Pixmap(fitz.csRGB, pix)
            pillowPix = convertToPillow1(pix)
            string = pytesseract.image_to_string(
                pillowPix,
                lang='por',
                config='--tessdata-dir .'
            )
            # annex the extracted data to the output
            output = output + ' ' + string
        # extract plain text from the file
        text = page.getText()
        # annext the extracted text to the output
        output = output + ' ' + text
    return output

# Extract data
import re
def extractData(path):
    """ Checks if the document is a PDF or a docx. If it's neither, return an error"""
    # declare as internal function (takes extension as argument, and returns true or false if it is)
    def assertExtension(fileName, extension):
        # create list of matches with match (regex pattern is \.{extension}$)
        matches = re.findall(f"\.{extension}$", fileName)
        # if the list has len == 0, return false
        if len(matches) == 0:
            return False
        # otherwise, return True
        else:
            return True
    # Verify extension
    # return string with extracted data
    if assertExtension(path, "pdf"):
        # if it's pdf, apply extractPDFData function
        return extractPDFData(path)
    elif assertExtension(path, "docx"):
        # if it's docx, apply extractDocxData function
        return extractDocxData(path)
    else:
        # if it's something else, raise ValueError exception
        raise ValueError(f"Invalid file format provided: {path}")
# In[ ]
# Clean data
def dataCleaning(fileString):
    """Use regular expressions to find the paragraph enumerations, and clean them up. Then also clean up the signature blanks"""
    import re
    # Use regex to detect \ndd \n patterns and delete them
    output = re.sub("\n\d* ", "", fileString)
    # Use regex to detect \ndd\n patterns and delete them
    output = re.sub("\n\d+", "", output)
    # Use regex to detect signatures, and delete them
    output = re.sub("_*", "", output)
    # New lines don't have any meaning here. Delete them
    output = output.replace("\n", " ")
    # Return cleaned fileString
    return output
# In[ ]
# On first version, do only /dataset/final/AtasCDINF
def saveToFile(file_path, file_string):
    with open(f"{file_path}.txt", "w", encoding="utf-8") as text_file:
        text_file.write(file_string)
# ex: saveToFile("ATA5", ata5_cleaned)
# Save resulting file into /dataset/final
# In[ ]
# Open all paths one by one and extract data from PDF or word
def preprocessFiles(pathList, originalExtension):
    # loop thru list of paths
    for path in pathList:
        # pass path to extractData function, take return value
        data = extractData(path)
        # clean extracted data
        data = dataCleaning(data)
        # save as file on final path
        # just replace the word raw with the word final in the path
        # also delete the file extension
        finalPath = path.replace("raw", "final").replace(originalExtension, "")
        saveToFile(finalPath, data)

preprocessFiles(files_pdf, ".pdf")
# In[ ]
# do the same for the docx files, just for sure
rawDOCX_dir = dataset_basedir + "\\raw\\AtasCDINF\\atasDOCX\\"
files_docx = listDirectory(rawDOCX_dir)
preprocessFiles(files_docx, ".docx")
# In[ ]

