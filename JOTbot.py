# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 12:40:01 2016

@author: josephwhite
"""
import nltk

from nltk.tokenize import word_tokenize as wt
from collections import defaultdict

class Node:
    def __init__(self, val):
        self.verb = None
        self.argument = None
        self.subject = val

dictionary = defaultdict(dict)

def is_goodbye(message):
    if message in ["bye", "Bye", "Goodbye", "Good-bye", "goodbye"]:
        return True
    else:
        return False

def is_rude(message):
    words = message.split()
    for word in words:
        if word in ["stupid", "Stupid", "boring", "Boring", "suck", "sucks"]:
            return True
    return False

def is_question(message):
    if message[-1] == "?":
        return True
    else:
        return False

def answer(question):
    tokenize = wt(question)
    pos = nltk.pos_tag(tokenize)

    subject = ""
    for tag in pos:
        if 'NNP' in tag:
            subject = tag[0]

    node = dictionary[subject]

    #Search for Subject in dictionary
    if subject and node.verb and node.argument != None:
        print "Yes I know, " + subject + " " + node.verb + " "+ node.argument
    else:
        print "Sorry I don't understand the question. Can you ask me another one?"


print "Hello, I am JOTBot."
while True:
    message = raw_input()
    tokenize = wt(message)
    if is_goodbye(message):
        break
    if is_rude(message):
        print "That's not nice"
    else:
        if is_question(message):
            answer(message)
        else:
            print "Ok"

            #Insert statement into table
            pos = nltk.pos_tag(tokenize)
            
            #Take first NNP
            if 'NNP' in pos[0][1]:
                n = Node(pos[0][0])
                # Take Verb
                if 'VB' or 'VBZ' in pos[1][0]:
                    n.verb = pos[1][0]

                adjunct = ""
                for x in range(2, len(pos)):
                    adjunct = adjunct + pos[x][0] + " "
                n.argument = adjunct

                dictionary[n.subject] = n
print "Goodbye"