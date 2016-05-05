# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:49:05 2016

@author: josephwhite
"""

from __future__ import division
#import nltk, re, pprint
from nltk import word_tokenize as wt
#from nltk import sent_tokenize
import random

class Node:
    def __init__(self, val):
        self.verb = None
        self.argument = None
        self.subject = val

e = {"bob": Node("Bob")}
#r = {"than": RelationNet}

def is_subject_pos(pos):
    if pos == 'NNP':
        return True
    if pos == 'NN':
        return True
    if pos == 'NNS':
        return True
    return False

def is_parrot_request(word):
    if word == "Say" or word == "say" or word == "Write" or word == "write":
        return True
    else:
        return False
        
def pick_fragment(entityDict, relationDict, sentence):
    # entityDict should match subjects to arguments
    # relationDict should match keys to RelationNets
        # each RelationNet stores relations between entities
    # put_frag? inc_frag? dec_frag? del_frag?
    r = random.random()
    if r < 0.1:
        print "That is interesting."
        return
    
    if is_parrot_request(sentence.split()[0]):
            s = ""
            for w in sentence.split()[1:]:
                s = s + " " + w
            print s
            return
            
    subjects = []        
    for word_tag_pair in nltk.pos_tag(wt(sentence)):
        #word = word_tag_pair[0]
        tag = word_tag_pair[1]
        # print word, tag               
        
        if tag == "VB":
            print "I don't take kindly to being ordered around."
            return

        if is_subject_pos(word_tag_pair[1]):
            subject = word_tag_pair[0]
            if subject.lower() not in e:
                subjects.append(subject)
                
    if len(subjects) != 0:
        print "Tell me more about " + random.sample(subjects, 1)[0] + "."
    else:
        print "Cool."
        
