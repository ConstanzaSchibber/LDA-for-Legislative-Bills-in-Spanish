'''
Created on May 29, 2014

LDA model 
You will need the corpus and the dictionary I created in the other file

@author: connieschibber
'''

from gensim import corpora, models 
import gensim
from gensim.corpora import MmCorpus, Dictionary
import numpy as np
import scipy
import numpy
import csv
import time
start_time = time.time()

#corpus_full = MmCorpus('corpus_ALL_argentina.mm')
#corpus_sample = MmCorpus('corpus_sample_argentina.mm') #for training set

dictionary = Dictionary.load('dict_all_argentina.dict')
print dictionary
#print corpus_full
#print corpus_sample

#Deciding the number of topics is more of an "art"
lda = gensim.models.ldamodel.LdaModel(corpus=corpus_sample, id2word=dictionary, num_topics=50, update_every=0, passes=75)
print time.time() - start_time, "seconds"
lda.save('/Users/connieschibber/RDirectory/Dissertation/ldamodel50TOPICS_sample')

# We print the topics
for i in range(0, lda.num_topics - 1):
    print lda.print_topic(i)

# Save the mixture of topics by document:
#in the Corpus/Dictionary code I created a csv file with the ID number of each bill 
#in order to attach this information to that

doc_topic = gensim.matutils.corpus2dense(lda[corpus_full], num_terms=lda.num_topics, num_docs=corpus_full.num_docs)

print 'ready to save'       
numpy.savetxt('DocBYTOPICArge_50Topics.csv', doc_topic, fmt='%10.10f', delimiter=',')
print time.time() - start_time, "seconds"

