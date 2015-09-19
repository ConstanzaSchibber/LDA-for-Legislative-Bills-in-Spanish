'''
Dictionary and Corpus for Bills introducted by legislators in Argentina
Language: Spanish
Created on Jun 3, 2014

@author: connieschibber
'''
import re
import glob
import codecs
import os
import random
import string
import nltk
import csv
import gensim
#from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize.regexp import WordPunctTokenizer
from gensim import corpora, models
from gensim.corpora import MmCorpus, Dictionary
import scipy
import numpy
import time

start_time = time.time()

#Import stopwords in txt file
stopwords_file = 'stopwords_es.txt'
stoplist = open(stopwords_file).read()

# Read data & create a spreadsheet with the name of each file (The name of each fill is the bill's official ID number)
datadir = #path to folder with all of the txt files

list_of_files = glob.glob(os.path.join(datadir, '*.txt'))
#sample_list = random.sample(list_of_files, 3)   #Use this is you want to try out the code with a sample of files 
sample_list = list_of_files

mynames = open('/Users/connieschibber/billheader.csv', 'w+')
writer = csv.writer(mynames, lineterminator='\n')

new_sample_list = []
for item in sample_list:
    item = os.path.basename(item)
    new_sample_list.append([item])
writer.writerows([new_sample_list])
mynames.close()

# Read each file (I use utf-16 due to file encoding)
def read_contents(filename):
    with codecs.open(filename, 'r', 'utf-16', 'ignore') as infile:
        return ' '.join(infile.readlines())

texts = [read_contents(filename) for filename in sample_list]
             
#files = [codecs.open(infile, 'r', 'utf-16', 'ignore') for infile in sample_list]#glob.glob(os.path.join(datadir, '*.txt'))]

#texts = [" ".join(file.readlines()[0:]) for file in files]
print 'files opened'
print time.time() - start_time, "seconds"

# Get rid of punctuation & tokenize
after_token = [[word.lower() for word in WordPunctTokenizer().tokenize(text) if word.lower() not in stoplist] for text in texts]
after_token = [[word for word in text if word not in string.punctuation] for text in after_token]

print time.time() - start_time, "seconds"    

all_tokens = sum(after_token, [])
print time.time() - start_time, "seconds"    

tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
print time.time() - start_time, "seconds"    

tokenised = [[word for word in text if word not in tokens_once] for text in after_token]

print 'tokenized'
print time.time() - start_time, "seconds"    

# first we create a dictionary containing a citation count for each word in each text
words = {}
for text in tokenised:
    for word in text:
        if words.has_key(word):
            words[word] += 1
        else:
            words[word] = 1
freq_word = [(w, words[w]) for w in words.keys()]

print freq_word
print time.time() - start_time, "seconds"    

# we order the word by frequency...
freq_word.sort(key=lambda tup: tup[1])

# ...then we sort them by descending order, meaning the most frequent come first
freq_word.reverse()
#print freq_word

# of those we keep only the most common, say the first 30
most_common = [x[0] for x in freq_word[:30]]

# and finally we exclude them from our corpus
print most_common
print time.time() - start_time, "seconds"    

tokenised = [[word for word in text if word not in most_common] for text in tokenised]

tokenised_new = []
for item in tokenised:    
    new = [x.encode('utf-8') for x in item]
    tokenised_new.append(new)
   
dictionary = corpora.Dictionary(tokenised_new)
print len(dictionary)
print dictionary
print time.time() - start_time, "seconds"    

dictionary.save('dict_all_argentina.dict')

#Now the corpus

corpus = [dictionary.doc2bow(text) for text in tokenised]

MmCorpus.serialize('/Users/connieschibber/RDirectory/Dissertation/corpus_all_argentina.mm', corpus)
